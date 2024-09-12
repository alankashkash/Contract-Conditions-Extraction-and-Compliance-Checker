# Contract Conditions Extraction and Compliance Checker

## Description
This project extracts financial terms from contract documents (PDF and DOCX) using OpenAI's API and checks compliance against a list of tasks provided in a CSV format. It aims to streamline the process of contract analysis and ensure that tasks align with the specified financial conditions.

## How It Works

1. **Contract Upload**: The user uploads a contract file in PDF or DOCX format. The app reads the contract and extracts key financial terms and conditions using OpenAI's API.

2. **Task List Upload**: The user uploads a CSV file containing a list of tasks. This file must include the columns `Task Description` and `Amount`, which detail the tasks to be analyzed against the contract terms.

3. **Processing**: Upon clicking the "Submit" button, the app processes the uploaded files:
   - It extracts terms from the contract and structures them in a JSON format.
   - It validates the tasks against the extracted contract terms to determine compliance. Each task is analyzed to see if it adheres to the specified financial conditions, such as budget limits and location-specific rules.

4. **Compliance Results**: The app generates a compliance report, indicating whether each task is "Compliant" or "Not Compliant." For non-compliant tasks, the app specifies the reasons for non-compliance, including any relevant terms from the contract and how much the task exceeds the allowable budget.

5. **Accuracy Evaluation**: The app also evaluates the accuracy of the compliance results against a predefined list of correct answers, providing an accuracy score to assess the performance of the compliance checking process.

6. **Output**: The results are displayed in a table format, allowing users to review the compliance status of each task easily.

This streamlined process helps users efficiently analyze contracts and ensure that their tasks align with the specified financial conditions.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/alankashkash/HerculesAI
   ```
2. Navigate to the project directory:
   ```bash
   cd HerculesAI
   ```
3. Install the required dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv pip install -r pyproject.toml
   ```
## Usage
1. Run the Streamlit interface:
   ```bash
   streamlit run interface.py
   ```
2. Upload the contract file (PDF or DOCX) and a CSV file containing tasks with the required columns: `Task Description` and `Amount`.
3. Click "Submit" to process the files. The compliance results will be displayed.