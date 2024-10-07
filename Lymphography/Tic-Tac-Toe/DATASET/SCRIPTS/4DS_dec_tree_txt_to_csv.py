import os
import pandas as pd
import glob

def collect_order_and_lengths(input_folder, output_folder):
    data = {}

    # Wzorzec nazwy pliku
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iteracja po wszystkich pasujących plikach
    for file in sorted(glob.glob(pattern)):
        # Wczytanie pliku CSV
        df = pd.read_csv(file)
        
        # Grupowanie po Order i zbieranie wszystkich długości
        grouped = df.groupby('Order')['Rule_Length'].apply(list)
        
        # Dodanie długości do słownika data
        for order, lengths in grouped.items():
            if order in data:
                data[order].extend(lengths)
            else:
                data[order] = lengths

    # Tworzenie i zapisywanie pliku CSV
    result = []
    max_lengths = max(len(lengths) for lengths in data.values())
    
    for order, lengths in data.items():
        row = {'Order': order}
        for i in range(max_lengths):
            if i < len(lengths):
                row[f'Length_{i+1}'] = lengths[i]
            else:
                row[f'Length_{i+1}'] = None  # lub możesz użyć 0 zamiast None
        result.append(row)

    # Konwersja listy słowników na DataFrame
    result_df = pd.DataFrame(result)

    # Sortowanie wyników po Order
    result_df = result_df.sort_values('Order')

    # Zapisanie do pliku CSV
    output_file = os.path.join(output_folder, 'order_and_lengths_summary.csv')
    result_df.to_csv(output_file, index=False)
    print(f"Zapisano plik: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/rules_output/'
output_folder = '../RESULTS/'

# Upewnij się, że folder wyjściowy istnieje
os.makedirs(output_folder, exist_ok=True)

collect_order_and_lengths(input_folder, output_folder)


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

# input_file = f"../RESULTS/3decision_rules.txt"
# output_file = f"../RESULTS/4decision_rules.csv"

# with open(input_file, "r") as file:
#     lines = file.readlines()


# attribute_set = set()
# for line in lines:
#     parts = line.strip().split(", class: ")[0]
#     conditions = parts.split(") & (")
#     conditions[0] = conditions[0][1:]
#     conditions[-1] = conditions[-1][:-1]
    
#     for condition in conditions:
#         attr_name = condition.split(" ")[0]
#         attribute_set.add(attr_name)

# attributes = list(attribute_set)
# attributes.sort() 
# attributes.append("Class")

# parsed_lines = [parse_line(line, attributes) for line in lines]


# with open(output_file, "w", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=attributes)
    
#     writer.writeheader()
#     for parsed_line in parsed_lines:
#         writer.writerow(parsed_line)

# print(f"Plik CSV został wygenerowany: {output_file}")
