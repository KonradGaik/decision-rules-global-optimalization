import os
import pandas as pd
import csv
from collections import defaultdict

def add_order_column(csv_file):
    output_file = csv_file.replace('.csv', '.csv')
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        total_rows = len(rows)

    with open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Order'] + rows[0])  # Write header with 'Order' as first column
        for idx, row in enumerate(rows[1:], start=1):
            writer.writerow([idx] + row)  # Write each row with its order index

    return output_file

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

    # Usuwanie duplikatów decyzji w każdej grupie
    for combination, decisions in decision_grouped.items():
        most_common_decision = max(set(decisions), key=decisions.count)
        decision_grouped[combination] = [most_common_decision]

    return decision_grouped

def save_to_csv_with_order(decision_grouped, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for combination, decisions in decision_grouped.items():
            for decision in decisions:
                row = list(combination) + [decision]
                writer.writerow(row)

# Ensure the output directories exist
for x in range(1, 6):
    output_dir = f'../RESULTS/subtable_{x}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# KROK 1 
# Utworzenie podtablic z reduktów
# Wczytaj plik CSV
df = pd.read_csv('../modified_lymphography.csv')

df = df[~df.apply(lambda row: all(value == 'c' for value in row), axis=1)]

reducts = [
    {'block_of_affere', 'changes_in_node', 'changes_in_stru', 'special_forms', 'dislocation_of', 'no_of_nodes_in'},
    {'block_of_affere', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'},
    {'block_of_affere', 'changes_in_lym', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_lym', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'}
]

# Process each reduct and add Order column
for idx, reduct in enumerate(reducts, start=1):
    df_selected = df[list(reduct) + ['class']]
    output_csv = os.path.join(f'../RESULTS/subtable_{idx}', f'1lymphography_reduct_subtable_{idx}.csv')
    df_selected.to_csv(output_csv, index=False)
    
    # Add Order column to the created CSV file
    output_with_order = add_order_column(output_csv)
    
    # Replace inconsistencies and save with Order
    decision_grouped = replace_inconsistencies(output_with_order)
    save_to_csv_with_order(decision_grouped, os.path.join(f'../RESULTS/subtable_{idx}', f'2consistent_modified_lymphography{idx}.csv'))

    print(f"Processed subtable {idx}: {output_csv}")
