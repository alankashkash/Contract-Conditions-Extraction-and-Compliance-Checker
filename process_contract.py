import openai
import PyPDF2
import docx
import os


def extract_terms_from_contract(contract_text, csv_file, client):
    csv_string = csv_file.read().decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"You're an expert in extracting key terms and analyzing task compliance with contract conditions. You will be provided with a contract text containing various terms and constraints for work execution, including budget constraints, allowable work types, financial terms, and location-specific rules (e.g., New York, Silicon Valley, Dubai) Any locations appearing in the contract you should mention explicitly using their names. Additionally, you will receive a CSV file with task descriptions and their respective cost estimates. Your task is to extract all key terms from the contract that are relevant to the conditions (e.g., budget limits, allowable expenses, payment terms, travel restrictions, and location-specific adjustments) and structure them in a JSON format. This JSON should reflect the contract’s sections and subsections for precise organization. The system will use this JSON to analyze each task description from the CSV for compliance with the contract's terms. If a task description violates any conditions (e.g., exceeding budget caps for New York travel, unapproved expenses in high-risk areas, or non-compliant work types), the system must identify the specific reason for the violation.\n\nContract: {contract_text}\n\nCSV File: {csv_string}"
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

def process_contract(uploaded_file, csv_file, api_key):
    # Read the contract file
    contract_text = read_contract_file(uploaded_file)

    # Extract terms
    terms = extract_terms_from_contract(contract_text, csv_file, api_key)

    return terms

