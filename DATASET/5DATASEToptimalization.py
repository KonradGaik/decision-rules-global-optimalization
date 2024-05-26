import os
import pandas as pd

def evaluate_rule(row_value, rule_value):
    # Usunięcie zbędnych nawiasów i spacji, jeśli istnieją
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    # Sprawdzenie, czy reguła jest w postaci warunku
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
        row_number = i + 1  # Numer wiersza w danych
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
                    if col_name != 'class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                        else:
                            is_matched = False
                            break
                    else:
                        if row[col_name] != int(rule_value):
                            is_matched = False
                            break
            if is_matched:
                matched_rules.append(rule[:-3] + f" => {rule_row['class']}")
        if matched_rules:
            matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    return matched_rows_df


for i in range(1, 6):
    # Ścieżki do plików danych i reguł
    csv_file_data = os.path.join(f"./", f"1consistent_lymphography.csv")
    csv_file_rules = os.path.join(f"./", f"3decision_rules_1.csv")
    
    # Wczytanie danych i reguł
    data_df = pd.read_csv(csv_file_data)
    rules_df = pd.read_csv(csv_file_rules)
    
    # Wywołanie funkcji match_rules_to_rows
    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    # Zapisanie wyniku do pliku CSV
    output_file = os.path.join(f"./", f"5matched_rows_shortest.csv")
    matched_rows.to_csv(output_file, index=False)
