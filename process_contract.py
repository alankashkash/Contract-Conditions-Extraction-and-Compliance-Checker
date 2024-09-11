import openai
import PyPDF2
import docx
import os


def extract_terms_from_contract(contract_text, api_key):
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"You're an expert in extracting conditions from the contract related to amounts of money.\n1. Conditions Extraction from the Contract:\nObjective: You will be provided with a contract text containing various terms and constraints for work execution that specifically relate to amounts of money (e.g., budget constraints, financial limits, payment terms, allowable expenses, etc.).\nTask:\n- Extract only the key terms that reference or are connected to amounts of money (e.g., total fees, payment stages, budget caps, allowances, or multipliers).\n- Structure the extracted terms in a JSON format.\n-Explicitly reflect specific locations, percentages, and conditions where applicable.\n- The JSON should organize the terms by relevant sections and subsections, reflecting their context in the contract.\nFocus Areas:\n- Budget constraints\n- Payment terms\n- Allowable expenses\n- Financial multipliers and adjustments\n- Any conditions that may affect the cost (e.g., late payments, budget caps, penalties).\n- Locations\n\nContract: {contract_text}"
                    }
                ]
            }
        ],
        max_tokens=4096,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def read_contract_file(uploaded_file):
    # Check the file type using the name attribute
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        contract_text = ""
        for page in reader.pages:
            contract_text += page.extract_text() + "\n"
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        contract_text = "\n".join([para.text for para in doc.paragraphs])
    
    return contract_text

def process_contract(uploaded_file, api_key):
    # Read the contract file
    contract_text = read_contract_file(uploaded_file)

    # Extract terms
    terms = extract_terms_from_contract(contract_text, api_key)

    return terms

def test_process_contract():
    API_KEY = os.getenv("OPENAI_API_KEY")
    file_path = "Contract + Amendment example v3 .docx"
    with open(file_path, "rb") as file:
        terms_json = process_contract(file, API_KEY)
        print(terms_json)

if __name__ == "__main__":
    test_process_contract()