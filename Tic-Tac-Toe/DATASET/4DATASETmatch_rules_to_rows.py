import pandas as pd
import os

def evaluate_rule(row_value, rule_value):
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    if '>' in rule_value:
        value = float(rule_value.split('>')[-1].strip())
        return row_value > value
    elif '<=' in rule_value:
        value = float(rule_value.split('<=')[-1].strip())
        return row_value <= value
    return False

def match_rules_to_rows(data_df, rules_df):
    matched_rows = []
    for i, row in data_df.iterrows():
        matched_rules = []
        matched_rule_strings = set() 
        for j, rule_row in rules_df.iterrows():
            rule = ""
            rule_length = 0
            is_matched = True
            for col_name, rule_value in rule_row.items():
                if pd.notna(rule_value):
                    if col_name != 'Class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                        else:
                            is_matched = False
                            break

            if is_matched and rule_length > 0:
                matched_rule_strings.add(rule)
                matched_rules.append({'Rule': rule[:-4] + f" => {rule_row['Class']}", 'Rule Length': rule_length})
    
        if matched_rules:
            matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})
    
    matched_rows_df = pd.DataFrame(matched_rows)
    matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
    matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    
    return matched_rows_df





csv_file_data = os.path.join(f"./", f"consistent_tic-tac-toe.csv")
csv_file_rules = os.path.join(f"./", f"decision_rules.csv")


data_df = pd.read_csv(csv_file_data, header=0)
rules_df = pd.read_csv(csv_file_rules, header=0)


matched_rows = match_rules_to_rows(data_df, rules_df)

output_file = os.path.join(f'./', f"matched_rows.csv")
matched_rows.to_csv(output_file, index=False)

print("Dopasowanie reguł zakończone sukcesem.")
