import streamlit as st
import pandas as pd
from process_contract import process_contract  # Import the process_contract function
from compliance_checker import validate_compliance  # Import the updated function
from internal_evaluation import evaluate_answers
import openai
import json  # Add this import

def main():
    st.title("Contract Conditions Extraction and Verification")

    # Input for OpenAI API key
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")

    # Upload file for Contract
    contract_file = st.file_uploader("Upload Contract (PDF, Docx)", type=["pdf", "docx"])

    # Upload file for List of Tasks
    tasks_file = st.file_uploader("Upload List of Tasks (CSV)", type=["csv"])

    # Process the inputs
    if st.button("Submit"):
        if api_key and contract_file and tasks_file:
            with st.spinner("Processing files..."):

                # Read the CSV file into a DataFrame
                tasks_df = pd.read_csv(tasks_file)

                # Validate required columns
                required_columns = ["Task Description", "Amount"]
                if not all(col in tasks_df.columns for col in required_columns):
                    st.error(f"CSV must contain the following columns: {', '.join(required_columns)}")
                else:
                    st.success("Files uploaded successfully!")
                    client = openai.OpenAI(api_key=api_key)
                    # Process the contract file and extract terms
                    terms_json = process_contract(contract_file, tasks_file, client)

                    st.write("Analysis of the provided tasks will appear under the generated JSON file. It's advisable to collapse JSON for better visibility.")
                    st.json(terms_json)

                    # Save the tasks DataFrame to a CSV file
                    tasks_csv_path = "tasks_data.csv"  # Specify the path
                    tasks_df.to_csv(tasks_csv_path, index=False)  # Save DataFrame to CSV

                    # Save the extracted terms to a JSON file
                    json_file_path = "extracted_terms.json"
                    with open(json_file_path, 'w') as json_file:
                        json_file.write(terms_json)

                    # Process the tasks DataFrame for compliance
                    updated_tasks_df = validate_compliance(tasks_csv_path, json_file_path, client)

                    accuracy_score = evaluate_answers(updated_tasks_df)
                    st.write(accuracy_score)

                    # Display the updated DataFrame
                    st.table(updated_tasks_df)
                    
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
