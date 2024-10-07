import csv
from collections import defaultdict
import os

def replace_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Wczytanie nagłówków
        for row in reader:
            attribute_combination = tuple(row[:-1])
            decision = row[-1]
            decision_grouped[attribute_combination].append(decision)

    # Usuwanie duplikatów decyzji w każdej grupie
    most_common_decisions = {}
    for combination, decisions in decision_grouped.items():
        most_common_decision = max(set(decisions), key=decisions.count)
        most_common_decisions[combination] = most_common_decision

    return most_common_decisions, headers

def save_to_csv(most_common_decisions, headers, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Zapisz nagłówki
        for combination, decision in most_common_decisions.items():
            row = list(combination) + [decision]
            writer.writerow(row)

# Tworzenie folderów jeśli nie istnieją
for x in range(1, 6):
    folder_path = f'../RESULTS/subtable_{x}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Przetwarzanie każdego pliku
for i in range(1, 6):
    csv_file = f"../RESULTS/subtable_{i}/1tic_tac_toe_reduct_subtable_{i}.csv"
    if os.path.exists(csv_file):
        most_common_decisions, headers = replace_inconsistencies(csv_file)
        save_to_csv(most_common_decisions, headers, f'../RESULTS/subtable_{i}', f"2consistent_modified_tic-tac-toe_{i}.csv")
    else:
        print(f"Plik {csv_file} nie istnieje.")
