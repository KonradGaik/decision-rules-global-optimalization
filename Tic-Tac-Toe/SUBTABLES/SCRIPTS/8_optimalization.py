import csv
import os
import pandas as pd

def evaluate_rule(data_value, rule_value):
    if pd.isna(data_value):
        return False
    else:
        return bool(data_value) == bool(rule_value)

def match_rules_to_rows(data_df, rules_df):
    matched_rows = []
    for i, row in data_df.iterrows():
        row_number = i + 1  
        matched_rules = []
        shortest_rule_length = float('inf')  # Inicjalizacja najkrótszej długości reguły jako nieskończoność
        for j, rule_row in rules_df.iterrows():
            rule = ""
            rule_length = 0
            is_matched = True
            for col_name, rule_value in rule_row.items():
                if pd.notna(rule_value):
                    if col_name not in row.index:
                        is_matched = False
                        break
                    if pd.isna(row[col_name]):
                        is_matched = False
                        break
                    if col_name != 'Class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                        else:
                            is_matched = False
                            rule = ""  # Zresetowanie ciągu rule w przypadku niezgodności
                            break
            if is_matched:
                if rule_length < shortest_rule_length:  # Aktualizacja najkrótszej długości reguły
                    shortest_rule_length = rule_length
                    matched_rules = [rule[:-3] + f" => {rule_row['Class']}"]
                elif rule_length == shortest_rule_length:  # Dodanie reguły o tej samej długości
                    matched_rules.append(rule[:-3] + f" => {rule_row['Class']}")
        if matched_rules:
            matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    return matched_rows_df



def process_files(base_rules_folder):
    for i in range(1, 6):
        csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"3consistent_encoded_modified_tic-tac-toe{i}.csv")
        csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"5decision_rules{i}.csv")
        
        data_df = pd.read_csv(csv_file_data)
        rules_df = pd.read_csv(csv_file_rules)

        matched_rows = match_rules_to_rows(data_df, rules_df)
        
        output_file = os.path.join(f"{base_rules_folder}{i}", f"8matched_rows_shortest_{i}.csv")
        with open(output_file, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Row Number', 'Matched Rules'])
            for _, row in matched_rows.iterrows():
                csv_writer.writerow([row['Row Number'], row['Matched Rules']])
        print("Output saved to", output_file)

if __name__ == "__main__":
    base_rules_folder = '../RESULTS/subtable_'
    process_files(base_rules_folder)
