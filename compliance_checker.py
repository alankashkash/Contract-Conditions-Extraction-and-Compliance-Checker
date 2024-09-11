import pandas as pd
import json

def check_compliance(row, terms_json):
    # Clean and convert 'Amount' for compliance check
    print(terms_json)
    amount_str = row['Amount'].replace('$', '').replace(',', '')  # Clean the string
    amount = float(amount_str)  # Convert to float

    # Placeholder function to check compliance against extracted terms
    if amount <= 3000:
        return "Compliant"
    else:
        return "Non-Compliant"

def process_tasks_df(tasks_df, terms_json):
    tasks_df['Compliance'] = tasks_df.apply(lambda row: check_compliance(row, terms_json), axis=1)
    return tasks_df  # Return the updated DataFrame


def test_process_tasks_csv(terms_json):
    input_csv_path = "Task example v3.xlsx - Sheet1.csv"  # Replace with your actual file name
    output_csv_path = "Task example v3_with_compliance.csv"
    tasks_df = pd.read_csv(input_csv_path)
    updated_tasks_df = process_tasks_df(tasks_df, terms_json)
    updated_tasks_df.to_csv(output_csv_path, index=False)
    print(f"Processed CSV saved to: {output_csv_path}")

if __name__ == "__main__":
    # Load terms from the contract for testing
    terms_json = json.loads('{"Budget Constraints": 10000, "Allowable Work Types": ["Consulting", "Development"]}')  # Example JSON
    test_process_tasks_csv(terms_json)