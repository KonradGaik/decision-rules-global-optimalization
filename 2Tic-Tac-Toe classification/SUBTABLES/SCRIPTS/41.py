# split_train_test.py
import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test(input_file, output_folder, test_size=0.3):
    df = pd.read_csv(input_file)
    X = df.drop(columns=['Class','Order'])
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
    pd.concat([X_train, y_train], axis=1).to_csv(f"{output_folder}/train.csv", index=False)
    pd.concat([X_test, y_test], axis=1).to_csv(f"{output_folder}/test.csv", index=False)
    print("Podzielono na zbiory treningowe i testowe.")

# Użycie
input_folder = "RESULTS"
for i in range(1, 6):
    input_file = f"../RESULTS/subtable_{i}/3encoded_tic_tac_toe_{i}.csv"
    output_folder = f"../{input_folder}/subtable_{i}"
    split_train_test(input_file, output_folder)
