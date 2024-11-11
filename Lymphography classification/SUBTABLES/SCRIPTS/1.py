# decision_table.py
import pandas as pd

def create_decision_table(input_file, output_file):
    df = pd.read_csv(input_file)
    df.to_csv(output_file, index=False)
    print("Tablica decyzji została zapisana:", output_file)

# Użycie
input_file = "../RESULTS/modified_lymphography.csv"
output_file = "../RESULTS/decision_table.csv"
create_decision_table(input_file, output_file)
