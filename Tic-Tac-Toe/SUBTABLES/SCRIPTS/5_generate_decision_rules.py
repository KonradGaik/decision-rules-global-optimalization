import os
import pandas as pd
import glob
import csv

def collect_order_lengths_and_rules(input_folder, output_file):
    # Słownik do przechowywania danych
    order_data = {}

    # Wzorzec nazwy pliku
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iteracja po wszystkich pasujących plikach
    for file in sorted(glob.glob(pattern)):
        # Wczytanie pliku CSV
        df = pd.read_csv(file)
        
        # Iteracja po wierszach DataFrame
        for _, row in df.iterrows():
            order = row['Order']
            length = int(row['Rule_Length'])  # Konwersja na int
            rule = row['Rule']
            
            # Jeśli Order już istnieje w słowniku, dodaj długość i regułę do list
            if order in order_data:
                order_data[order]['lengths'].append(length)
                order_data[order]['rules'].append(rule)
            else:
                # Jeśli nie, utwórz nowe listy z tą długością i regułą
                order_data[order] = {'lengths': [length], 'rules': [rule]}

    # Tworzenie listy wyników
    result = []
    max_length = max(len(data['lengths']) for data in order_data.values())
    
    for order, data in order_data.items():
        row = {'Order': order}
        for i in range(max_length):
            if i < len(data['lengths']):
                row[f'Length_{i+1}'] = data['lengths'][i]
                row[f'Rule_{i+1}'] = data['rules'][i]
            else:
                row[f'Length_{i+1}'] = ''
                row[f'Rule_{i+1}'] = ''
        result.append(row)

    # Sortowanie wyników po Order
    result.sort(key=lambda x: x['Order'])

    # Zapisanie do pliku CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Order'] + [f'Length_{i+1}' for i in range(max_length)] + [f'Rule_{i+1}' for i in range(max_length)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    print(f"Zapisano zbiorczy plik: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/combined_rules/'
output_file = '../RESULTS/order_lengths_and_rules_summary.csv'

collect_order_lengths_and_rules(input_folder, output_file)
# import csv
# import re

# def parse_line(line, attributes):
#     parts = line.strip().split(", class: ")
#     class_label = parts[1]
#     conditions = parts[0].split(") & (")
#     conditions[0] = conditions[0][1:]
#     conditions[-1] = conditions[-1][:-1]
    
#     condition_dict = {attr: "" for attr in attributes}
#     condition_dict["Class"] = class_label
#     for condition in conditions:
#         for key in condition_dict.keys():
#             if key in condition:
#                 condition_dict[key] = condition.strip()
#                 break
    
#     return condition_dict
# for i in range(1,6):
#     input_file = f"../RESULTS/subtable_{i}/4decision_rules_{i}.txt"
#     output_file = f"../RESULTS/subtable_{i}/5decision_rules{i}.csv"

#     with open(input_file, "r") as file:
#         lines = file.readlines()

#     attribute_set = set()
#     for line in lines:
#         parts = line.strip().split(", class: ")[0]
#         conditions = parts.split(") & (")
#         conditions[0] = conditions[0][1:] 
#         conditions[-1] = conditions[-1][:-1]
        
#         for condition in conditions:
#             attr_name = condition.split(" ")[0]
#             attribute_set.add(attr_name)

#     attributes = list(attribute_set)
#     attributes.sort()
#     attributes.append("Class")

#     parsed_lines = [parse_line(line, attributes) for line in lines]
 
#     with open(output_file, "w", newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=attributes)
        
#         writer.writeheader()
#         for parsed_line in parsed_lines:
#             writer.writerow(parsed_line)

#     print(f"Plik CSV został wygenerowany: {output_file}")
