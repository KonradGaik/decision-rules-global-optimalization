import csv
from collections import defaultdict
import os

def replace_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if all(value == "c" for value in row):
                continue
            attribute_combination = tuple(row[:-1])
            decision = row[-1]
            decision_grouped[attribute_combination].append(decision)

    for combination, decisions in decision_grouped.items():
        most_common_decision = max(set(decisions), key=decisions.count)
        for i, decision in enumerate(decisions):
            if decision != most_common_decision:
                decisions[i] = most_common_decision

    return decision_grouped


def save_to_csv(decision_grouped, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for combination, decisions in decision_grouped.items():
            for decision in decisions:
                row = list(combination) + [decision]
                writer.writerow(row)

csv_file = f"./encoded_tic_tac_toe.csv"
decision_grouped = replace_inconsistencies(csv_file)
save_to_csv(decision_grouped, f'.', f"consistent_tic-tac-toe.csv")
