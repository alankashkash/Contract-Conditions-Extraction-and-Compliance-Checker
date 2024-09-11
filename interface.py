import streamlit as st
import pandas as pd
from process_contract import process_contract  # Import the process_contract function
from compliance_checker import process_tasks_df  # Import the updated function

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

                    # Process the contract file and extract terms
                    terms_json = process_contract(contract_file, api_key)

                    # Display the extracted terms
                    st.json(terms_json)

                    # Process the tasks DataFrame for compliance
                    updated_tasks_df = process_tasks_df(tasks_df, terms_json)

                    # Display the updated DataFrame
                    st.table(updated_tasks_df)
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
