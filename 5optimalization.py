import os
import pandas as pd

def evaluate_rule(row_value, rule_value):
    # Usunięcie zbędnych nawiasów i spacji, jeśli istnieją
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    # Sprawdzenie czy reguła jest w postaci warunku
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
        matched_rules = []  # Zainicjowanie pustej listy pasujących reguł dla danego wiersza
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
                matched_rules.append({'Rule': rule[:-3] + f" => {rule_row['class']}", 'Rule Length': rule_length})
        if matched_rules:
            matched_rules.sort(key=lambda x: x['Rule Length'])  # Sortowanie reguł względem długości
            matched_rows.append({'Row Number': i + 1, 'Shortest Matched Rule': matched_rules[0]})
    matched_rows_df = pd.DataFrame(matched_rows)
    # Rozwijanie kolumny 'Shortest Matched Rule' do osobnych kolumn
    matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Shortest Matched Rule'].tolist()))
    return matched_rows_df.drop(columns=['Shortest Matched Rule'])  # Usunięcie kolumny tymczasowej

# Iteracja po wszystkich plikach w folderze
for i in range(1, 6):  # Zakładając, że pliki są ponumerowane od 1 do 5
    # Wczytanie danych z plików CSV
    data_df = pd.read_csv(f'2consistent_data/consistent_modified_lymphography{i}.csv')
    rules_df = pd.read_csv(f'3decision_rules/decision_rules_{i}_2.csv')
    
    # Wywołanie funkcji match_rules_to_rows
    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    # Zapisanie wyniku do pliku CSV
    matched_rows.to_csv(f'matched_rows_shortest_{i}.csv', index=False)
