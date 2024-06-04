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
    else:
        return False

def match_rules_to_rows(data_df, rules_df):
    matched_rows = []
    for i, row in data_df.iterrows():
        row_number = i + 1  
        matched_rules = []
        for j, rule_row in rules_df.iterrows():
            rule = ""
            rule_length = 0
            is_matched = True
            for col_name, rule_value in rule_row.items():
                if pd.notna(rule_value):
                    if col_name not in row.index:
                        print(f"Column {col_name} not found in data_df at row {i}")
                        is_matched = False
                        break
                    if pd.isna(row[col_name]):
                        is_matched = False
                        break
                    if col_name != 'class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                        else:
                            is_matched = False
                            break
     
            if is_matched:
                matched_rules.append(rule[:-3] + f" => {rule_row['class']}")
        if matched_rules:
            matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    return matched_rows_df

base_rules_folder = 'subtable_'

for i in range(1, 6):
    csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"consistent_modified_tic-tac-toe{i}.csv")
    csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"decision_rules{i}.csv")
    
    data_df = pd.read_csv(csv_file_data)
    rules_df = pd.read_csv(csv_file_rules)
    
    # Rename 'Class' column to 'class' in data_df to match rules_df
    if 'Class' in data_df.columns:
        data_df.rename(columns={'Class': 'class'}, inplace=True)
    
    # Display the column names for debugging
    print(f"Columns in data_df for subtable_{i}:", data_df.columns)
    print(f"Columns in rules_df for subtable_{i}:", rules_df.columns)
    
    if 'class' not in data_df.columns:
        print(f"Column 'class' not found in data_df for subtable_{i}")
        continue

    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    output_file = os.path.join(f"{base_rules_folder}{i}", f"matched_rows_shortest_{i}.csv")
    matched_rows.to_csv(output_file, index=False)
