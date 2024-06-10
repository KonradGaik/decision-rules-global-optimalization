import os
import pandas as pd

def evaluate_rule(row_value, rule_value):
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    if '>' in rule_value:
        value = float(rule_value.split('>')[-1].strip())
        return row_value > value
    elif '<=' in rule_value:
        value = float(rule_value.split('<=')[-1].strip())
        return row_value <= value
    return False


def find_shortest_rule_length(rules_df):
    min_length = float('inf')  # Ustaw początkową najkrótszą długość na nieskończoność

    for _, rule_row in rules_df.iterrows():
        # Oblicz długość reguły jako liczbę niepustych wartości w wierszu
        rule_length = rule_row.count()

        # Jeśli obecna długość reguły jest krótsza niż dotychczas znaleziona najkrótsza, zaktualizuj najkrótszą długość
        if rule_length < min_length:
            min_length = rule_length

    return min_length

def match_rules_to_rows(data_df, rules_df):
    matched_rows = []
    shortest_rule_length = find_shortest_rule_length(rules_df)
    for i, row in data_df.iterrows():
        matched_rules = []
        #print(row)
        matched_rule_strings = set()  # Zbiór dla unikalnych łańcuchów reguł
        
        for j, rule_row in rules_df.iterrows():
            rule = ""
            rule_length = 0
            for col_name, rule_value in rule_row.items():
                if pd.isnull(rule_value):
                    continue
                if pd.notna(rule_value):
                    if col_name != 'Class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                            is_matched = True
                        else:
                            is_matched = False
                    else:
                        if str(row[col_name]) != str(rule_value):
                            is_matched = False
                            break
            rule_row_set = set(rule_row)
            rule_set = set(rule.split(" && "))
            # if i == 0 and j == 0:
            #     print(f'TEST1: {rule_row_set}, TEST2: {rule_set}')
            if is_matched and rule_length >= shortest_rule_length and pd.notna(rule_row_set.issubset(rule_set)):
                if rule not in matched_rule_strings:
                    matched_rule_strings.add(rule)
                    matched_rules.append({'Rule': rule[:-4] + f" => {rule_row['Class']}", 'Rule Length': rule_length})
        if matched_rules:
            matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
    matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    
    return matched_rows_df


# def match_rules_to_rows(data_df, rules_df):
#     matched_rows = []
#     for i, row in data_df.iterrows():
#         row_number = i + 1  
#         matched_rules = []
#         for j, rule_row in rules_df.iterrows():
#             rule = ""
#             rule_length = 0
#             is_matched = True
#             for col_name, rule_value in rule_row.items():
#                 if pd.notna(rule_value):
#                     if col_name not in row.index:
#                         print(f"Column {col_name} not found in data_df at row {i}")
#                         is_matched = False
#                         continue
#                     if pd.isna(row[col_name]):
#                         is_matched = False
#                         continue
#                     if col_name != 'Class':
#                         if evaluate_rule(row[col_name], rule_value):
#                             rule += f"{rule_value} && "
#                             rule_length += 1
#                         else:
#                             is_matched = False
#                             continue
     
#             if is_matched:
#                 matched_rules.append(rule[:-3] + f" => {rule_row['Class']}")
#         if matched_rules:
#             matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
#     matched_rows_df = pd.DataFrame(matched_rows)
#     return matched_rows_df


# Foldery z danymi i regułami
base_rules_folder = '../RESULTS/subtable_'

output_folder = '../RESULTS/subtable_'
os.makedirs(output_folder, exist_ok=True)

# Iteracja po folderach subtable1, subtable2, ..., subtable5
for i in range(1, 6):
    # Ścieżki do plików danych i reguł
    csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"3consistent_encoded_modified_tic-tac-toe{i}.csv")
    csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"5decision_rules{i}.csv")
    
    # Wczytanie danych i reguł
    data_df = pd.read_csv(csv_file_data)
    rules_df = pd.read_csv(csv_file_rules)
    
    # Dopasowanie reguł do wierszy
    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    # Zapisanie wyników do pliku
    output_file = os.path.join(f'{output_folder}{i}', f"6matched_rows{i}.csv")
    matched_rows.to_csv(output_file, index=False)