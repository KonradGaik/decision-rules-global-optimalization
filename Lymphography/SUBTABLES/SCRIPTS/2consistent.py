import csv
from collections import defaultdict
import os

def remove_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    header = None  # Initialize header variable
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        header_without_order = header[1:]  # Remove the first column
        
        for row in reader:
            attributes = tuple(row[1:])  # All columns except the first one
            order = row[0]  # First column (Order)
            decision_grouped[attributes].append(order)
    
    # Remove inconsistencies and keep most common order value for each attribute combination
    cleaned_data = {}
    for attributes, orders in decision_grouped.items():
        if len(set(orders)) == 1:
            cleaned_data[attributes] = orders[0]  # Only one unique order, keep it
        else:
            most_common_order = max(set(orders), key=orders.count)
            cleaned_data[attributes] = most_common_order
    
    return cleaned_data, header_without_order  # Return cleaned data and header without the first column

def save_cleaned_data(cleaned_data, header, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)
    
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        for attributes, order in cleaned_data.items():
            row = [order] + list(attributes)
            writer.writerow(row)

# Process each subtable and save the modified results
for i in range(1, 6):
    input_csv = f"../RESULTS/subtable_{i}/1lymphography_reduct_subtable_{i}.csv"
    output_folder = f"../RESULTS/subtable_{i}"
    output_file = f"2consistent_modified_lymphography{i}.csv"
    
    cleaned_data, header = remove_inconsistencies(input_csv)
    save_cleaned_data(cleaned_data, header, output_folder, output_file)
    
    print(f"Processed subtable {i} and saved cleaned data.")
