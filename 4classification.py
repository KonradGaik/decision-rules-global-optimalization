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
            matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})
    matched_rows_df = pd.DataFrame(matched_rows)
    # Konwersja listy słowników w kolumnę krotek
    matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
    # Rozwijanie kolumny 'Matched Rules' do osobnych kolumn
    matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    return matched_rows_df

folder_name_data = '2consistent_data'
folder_name_rules = '3decision_rules'

output_folder = '4results'

# Iteracja po wszystkich plikach w folderze
for i in range(1, 6):  # Zakładając, że pliki są ponumerowane od 1 do 5
    # Utworzenie ścieżek do plików CSV
    csv_file_data = os.path.join(folder_name_data, f"consistent_modified_lymphography{i}.csv")
    csv_file_rules = os.path.join(folder_name_rules, f"decision_rules_{i}_2.csv")
    
    # Wczytanie danych z plików CSV
    data_df = pd.read_csv(csv_file_data)
    rules_df = pd.read_csv(csv_file_rules)
    
    # Wywołanie funkcji match_rules_to_rows
    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    # Zapisanie wyniku do pliku CSV
    output_file = os.path.join(output_folder, f"matched_rows_{i}.csv")
    matched_rows.to_csv(output_file, index=False)
