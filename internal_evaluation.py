import pandas as pd

def evaluate_answers(data):
    data = data.copy()
    correct_answers = [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
    data['Compliance Binary'] = data['Compliance'].apply(lambda x: 1 if x.strip().lower() == "compliant" else 0)
    compliance_list = data['Compliance Binary'].tolist()
    accuracy_score = sum(compliance_list[i] == correct_answers[i] for i in range(len(correct_answers))) / len(correct_answers)
    return f"Accuracy Score: {accuracy_score:.2f}"

