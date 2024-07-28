

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

# import os
# import pandas as pd

# def evaluate_rule(row_value, rule_value):
#     rule_value = rule_value.replace('(', '').replace(')', '').strip()
#     if '>' in rule_value:
#         value = float(rule_value.split('>')[-1].strip())
#         return row_value > value
#     elif '<=' in rule_value:
#         value = float(rule_value.split('<=')[-1].strip())
#         return row_value <= value
#     return False


# def find_shortest_rule_length(rules_df):
#     min_length = float('inf') 

#     for _, rule_row in rules_df.iterrows():
#         rule_length = rule_row.count()

#         if rule_length < min_length:
#             min_length = rule_length

#     return min_length

# def match_rules_to_rows(data_df, rules_df):
#     matched_rows = []
#     shortest_rule_length = find_shortest_rule_length(rules_df)
#     for i, row in data_df.iterrows():
#         matched_rules = []
#         matched_rule_strings = set()  
#         for j, rule_row in rules_df.iterrows():
#             rule = ""
#             rule_length = 0
#             for col_name, rule_value in rule_row.items():
#                 if pd.isnull(rule_value):
#                     continue
#                 if pd.notna(rule_value):
#                     if col_name != 'Class':
#                         if evaluate_rule(row[col_name], rule_value):
#                             rule += f"{rule_value} && "
#                             rule_length += 1
#                             is_matched = True
#                         else:
#                             is_matched = False
#                     else:
#                         if str(row[col_name]) != str(rule_value):
#                             is_matched = False
#                             break
#             rule_row_set = set(rule_row)
#             rule_set = set(rule.split(" && "))
#             if is_matched and rule_length >= shortest_rule_length and pd.notna(rule_row_set.issubset(rule_set)):
#                 if rule not in matched_rule_strings:
#                     matched_rule_strings.add(rule)
#                     matched_rules.append({'Rule': rule[:-4] + f" => {rule_row['Class']}", 'Rule Length': rule_length})
#         if matched_rules:
#             matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})
#     matched_rows_df = pd.DataFrame(matched_rows)
#     if 'Matched Rules' in matched_rows_df.columns:
#         matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
#         matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    
#     return matched_rows_df


# # def match_rules_to_rows(data_df, rules_df):
# #     matched_rows = []
# #     for i, row in data_df.iterrows():
# #         row_number = i + 1  
# #         matched_rules = []
# #         for j, rule_row in rules_df.iterrows():
# #             rule = ""
# #             rule_length = 0
# #             is_matched = True
# #             for col_name, rule_value in rule_row.items():
# #                 if pd.notna(rule_value):
# #                     if col_name not in row.index:
# #                         print(f"Column {col_name} not found in data_df at row {i}")
# #                         is_matched = False
# #                         continue
# #                     if pd.isna(row[col_name]):
# #                         is_matched = False
# #                         continue
# #                     if col_name != 'Class':
# #                         if evaluate_rule(row[col_name], rule_value):
# #                             rule += f"{rule_value} && "
# #                             rule_length += 1
# #                         else:
# #                             is_matched = False
# #                             continue
     
# #             if is_matched:
# #                 matched_rules.append(rule[:-3] + f" => {rule_row['Class']}")
# #         if matched_rules:
# #             matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
# #     matched_rows_df = pd.DataFrame(matched_rows)
# #     return matched_rows_df


# base_rules_folder = '../RESULTS/subtable_' 
# output_folder = '../RESULTS/subtable_'
# os.makedirs(output_folder, exist_ok=True)

# for i in range(1, 6):
#     csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"3consistent_encoded_modified_tic-tac-toe{i}.csv")
#     csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"5decision_rules{i}.csv")
    
#     data_df = pd.read_csv(csv_file_data)
#     rules_df = pd.read_csv(csv_file_rules)
    
#     matched_rows = match_rules_to_rows(data_df, rules_df)

#     output_file = os.path.join(f'{output_folder}{i}', f"6matched_rows{i}.csv")
#     matched_rows.to_csv(output_file, index=False)