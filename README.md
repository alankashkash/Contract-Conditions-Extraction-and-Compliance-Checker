# Contract Conditions Extraction and Compliance Checker

## Description
This project extracts financial terms from contract documents (PDF and DOCX) using OpenAI's API and checks compliance against a list of tasks provided in a CSV format. It aims to streamline the process of contract analysis and ensure that tasks align with the specified financial conditions.

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