import os
import pandas as pd
import ast

def process_files(base_rules_folder):
    for i in range(1, 6):
        csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"7matched_rows_unique{i}.csv")
        data_df = pd.read_csv(csv_file_data)
        shortest_rules_df = match_rules_to_rows(data_df)
        shortest_rules_df.to_csv(os.path.join(f"{base_rules_folder}{i}", f"8matched_rows_shortest_{i}.csv"), index=False)

def match_rules_to_rows(data_df):
    matched_rows = []
    for i, row in data_df.iterrows():
        row_number = i + 1  
        matched_rules = ast.literal_eval(row['Matched Rules'])
        shortest_rule_length = min(len(rule['Rule'].split('&&')) for rule in matched_rules)
        shortest_rules = [rule for rule in matched_rules if len(rule['Rule'].split('&&')) == shortest_rule_length]
        matched_rows.append({'Row Number': row_number, 'Shortest Rules': shortest_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    return matched_rows_df

if __name__ == "__main__":
    base_rules_folder = '../RESULTS/subtable_'
    process_files(base_rules_folder)