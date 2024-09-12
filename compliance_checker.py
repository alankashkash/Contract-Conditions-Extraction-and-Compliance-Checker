import pandas as pd
from io import BytesIO

def validate_compliance(csv_file_path, json_file_path, client):
  json_file = client.files.create(
    file=open(json_file_path, "rb"),
    purpose='assistants'
  )
  csv_file = client.files.create(
    file=open(csv_file_path, "rb"),
    purpose='assistants'
  )

  assistant = client.beta.assistants.create(
    name="Compliance Guardian",
    instructions="""You're an expert in analyzing task compliance with contract terms using provided JSON data and a code interpreter. - Input: You will be provided with two files: 1. A JSON file containing the key terms from a contract, such as budget constraints, allowable expenses, location-specific rules, and other financial conditions. 2. A CSV file containing task descriptions and their respective cost estimates. - Objective: Your task is to validate all tasks in the CSV against the contract conditions outlined in the JSON file. Each row in the CSV will include a task and an amount of money assigned to it. - Execution: Instead of processing each task row by row, you should process all rows in one operation by using a for-loop internally with the code interpreter. - For each row, compare the task and amount to the corresponding terms in the JSON (e.g., budget caps, location-specific rules, or other financial constraints). - Output: Store the result of the compliance check (either "compliant" or "not compliant", with the reason for non-compliance) in a new column labeled "Compliance" for each row. - You should return othe CSV file with the "Compliance" column filled for every row, indicating whether the task is compliant with the contract terms. Do not return empty fields, if everything is ok you should fill the "Compliance" column with the word "Compliant". Return the content as a downloadable csv file.""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
    tool_resources={
      "code_interpreter": {
        "file_ids": [json_file.id, csv_file.id]
      }
    }
  )

  thread = client.beta.threads.create()

  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Please analyze the provided files and return the .csv file"
  )

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
  )

  if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )

    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Please revise the Compliance column in the file you generated using the provided JSON file to validate whether you checked compliance for every task correctly. If not, correct your mistake and return a file with corrected values. In the message list all the changes you have made. If the initial version was correct from the start let me know about that too."
  )
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )
    if run.status == 'completed': 
      print(messages.data[0].content[0].text.value)
      file_id = messages.data[0].attachments[0].file_id
      csv_data = client.files.content(file_id)
      byte_content = csv_data.read()
      df = pd.read_csv(BytesIO(byte_content))
      return df    
  else:
    raise ValueError(f"Run status: {run.status}")
  
if __name__ == "__main__":
  import openai, os
  client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  df = validate_compliance("/Users/alankashkash/PycharmProjects/HerculesAI/tasks_data.csv", "/Users/alankashkash/PycharmProjects/HerculesAI/extracted_terms.json", client)
  print(df)