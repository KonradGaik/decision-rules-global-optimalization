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
                    if pd.isna(row[col_name]):
                        is_matched = False
                        break
                    if col_name != 'Class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                            
                        else:
                            is_matched = False
                            break
          
            if is_matched:
                matched_rules.append(rule[:-3] + f" => {rule_row['Class']}")
        if matched_rules:
            matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    return matched_rows_df


for i in range(1, 6):

    csv_file_data = os.path.join(f"./", f"encoded_tic_tac_toe.csv")
    csv_file_rules = os.path.join(f"./", f"decision_rules.csv")

    data_df = pd.read_csv(csv_file_data)
    rules_df = pd.read_csv(csv_file_rules)
    
    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    output_file = os.path.join(f"./", f"5matched_rows_shortest.csv")
    matched_rows.to_csv(output_file, index=False)
