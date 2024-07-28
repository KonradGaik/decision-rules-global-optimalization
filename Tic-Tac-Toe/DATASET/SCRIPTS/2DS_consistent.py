import csv
from collections import defaultdict
import os

def remove_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    header = None
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        for row in reader:
            if all(value == "c" for value in row):
                continue
            attribute_combination = tuple(row[:-1])  # All columns except the last one
            decision = row[-1]  # Last column is the decision
            decision_grouped[attribute_combination].append(decision)

    cleaned_data = {}
    for combination, decisions in decision_grouped.items():
        if len(set(decisions)) == 1:
            cleaned_data[combination] = decisions[0]  # Only one unique decision, keep it
        else:
            most_common_decision = max(set(decisions), key=decisions.count)
            cleaned_data[combination] = most_common_decision

    return cleaned_data, header

def save_to_csv(cleaned_data, header, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the original header
        for combination, decision in cleaned_data.items():
            row = list(combination) + [decision]
            writer.writerow(row)

csv_file = "../RESULTS/1encoded_tic_tac_toe.csv"
cleaned_data, header = remove_inconsistencies(csv_file)
save_to_csv(cleaned_data, header, "../RESULTS", "2consistent_tic-tac-toe.csv")

print("Processed data and removed inconsistencies.")