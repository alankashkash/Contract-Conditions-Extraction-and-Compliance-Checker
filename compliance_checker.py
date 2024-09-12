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
    instructions = "You're an expert in analyzing task compliance with contract terms using provided JSON data and a code interpreter. - Input: You will be provided with two files: 1. A JSON file containing key terms from the contract as a string. 2. A CSV file containing task descriptions and their respective cost estimates. - Objective: Your task is to use the JSON as a lookup table to identify if there are any terms (e.g., location-specific rules, seasonal adjustments, special circumstances, etc.) that relate to each task description in the CSV. For each task, identify relevant terms from the JSON string, and apply all applicable multipliers or adjustments **to the base budget of $2,500** to compute the total allowable budget for the task. Then, compare this computed budget with the task's amount. If the task is compliant, return 'Compliant'. If the task is not compliant, return 'Not Compliant', and specify the reason for the violation, including any relevant terms from the JSON and how much the task exceeds the calculated budget cap. - Execution: Process all rows in one operation by using a for-loop internally with the code interpreter. Ensure that for each row, you apply the relevant multipliers to the **base budget** ($2,500) and not the task's amount. Cross-check the task description with all relevant terms in the JSON string before making a compliance decision. Be aware that multiple terms can apply to the same task. Ensure that all relevant terms are taken into account (e.g., location, seasonal adjustment, special circumstances) and apply each multiplier accordingly. - Output: Store the result of the compliance check in a new column labeled 'Compliance' for each row. For non-compliant tasks, the output must specify the reason for non-compliance, including relevant terms and the computed budget cap.",
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
    # file_id = messages.data[0].attachments[0].file_id
    messages = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Please modify the CSV file to include an additional column labeled 'Ambiguous'. This column should flag ambiguous cases where it is unclear from the description of the task whether it may contradict the contract terms. Specifically: - If the task description includes vague or ambiguous terms (e.g., unclear location, time, or special circumstances), mark the task as 'Ambiguous'. - Use the JSON as a lookup table and, if no clear match is found or if there are conflicting interpretations of the task, mark the task as 'Ambiguous'. - The 'Ambiguous' column should contain either 'Yes' or 'No' for each task, with 'Yes' indicating the need for further clarification.",
    # file_id=file_id
  )
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )
    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
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