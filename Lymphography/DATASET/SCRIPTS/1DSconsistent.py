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
            attribute_combination = tuple(row[1:])  # Exclude the first column (Order)
            order = row[0]  # First column is Order
            decision_grouped[attribute_combination].append(order)

    cleaned_data = {}
    for combination, orders in decision_grouped.items():
        if len(set(orders)) == 1:
            cleaned_data[combination] = orders[0]  # Only one unique order, keep it
        else:
            most_common_order = max(set(orders), key=orders.count)
            cleaned_data[combination] = most_common_order

    return cleaned_data, header

def save_to_csv(cleaned_data, header, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['No.'] + header)  # Add 'No.' to the header
        for index, (combination, order) in enumerate(cleaned_data.items(), start=1):
            row = [index, order] + list(combination)
            writer.writerow(row)

csv_file = "../RESULTS/consistent_modified_lymphography.csv"
cleaned_data, header = remove_inconsistencies(csv_file)
save_to_csv(cleaned_data, header, "../RESULTS", "1consistent_lymphography.csv")

print("Processed data and removed inconsistencies.")