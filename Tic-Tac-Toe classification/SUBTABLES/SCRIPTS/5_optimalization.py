import os
import pandas as pd
import glob
import csv

def find_shortest_rules(input_folder, output_file):
    # Dictionary to store data for shortest rules
    shortest_rules_data = {}

    # Pattern for rule files
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iterate over all matching files
    for file in sorted(glob.glob(pattern)):
        # Read the CSV file
        df = pd.read_csv(file)

        # Check if required columns exist
        if 'Order' not in df.columns or 'Rule_Length' not in df.columns:
            print(f"Skipping {file} due to missing columns.")
            continue  # Skip this file if columns are missing

        # Iterate over DataFrame rows
        for _, row in df.iterrows():
            order = row['Order']
            length = int(row['Rule_Length'])  # Convert to int
            rule = row['Rule']
            class_label = row['Class'] if 'Class' in row else None  # Safe assignment of class

            # If the order doesn't exist in the dictionary, add it
            if order not in shortest_rules_data:
                shortest_rules_data[order] = {'length': length, 'rules': [rule], 'class': class_label}
            else:
                # If the current rule length is shorter, replace the list with this rule
                if length < shortest_rules_data[order]['length']:
                    shortest_rules_data[order] = {'length': length, 'rules': [rule], 'class': class_label}
                # If the current rule length is equal, append the rule to the list
                elif length == shortest_rules_data[order]['length']:
                    shortest_rules_data[order]['rules'].append(rule)

    # Check if shortest_rules_data is empty
    if not shortest_rules_data:
        print("No valid rules found.")
        return  # Exit the function if no valid rules were found

    # Create a list to store the results
    result = []
    for order, data in shortest_rules_data.items():
        row = {'Order': order, 'Length': data['length'], 'Class': data['class']}
        for i, rule in enumerate(data['rules'], start=1):
            row[f'Rule_{i}'] = rule
        result.append(row)

    # Sorting results by Order
    result.sort(key=lambda x: x['Order'])

    # Find the maximum number of rules across all orders, only if there is data
    max_rules = max((len(data['rules']) for data in shortest_rules_data.values()), default=0)

    # Save the shortest rules to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Order', 'Length', 'Class'] + [f'Rule_{i+1}' for i in range(max_rules)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in result:
            writer.writerow(row)

# Set the input folder containing rule files and output summary file location
input_folder = '../RESULTS/combined_rules/'
output_file = os.path.join('../RESULTS', 'shortest_rules_summary.csv')

# Run the function to find the shortest rules for each order
find_shortest_rules(input_folder, output_file)

print(f"Summary of shortest rules saved to {output_file}")
