import os
import pandas as pd
import glob
import csv

def collect_shortest_rules(input_folder, output_file):
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
            length = int(row['Rule_Length'])
            rule = row['Rule']
            
            # Jeśli Order już istnieje w słowniku
            if order in order_data:
                if length < order_data[order]['min_length']:
                    # Jeśli znaleziono krótszą regułę, zastąp wszystkie dotychczasowe
                    order_data[order] = {'min_length': length, 'rules': set([rule])}
                elif length == order_data[order]['min_length']:
                    # Jeśli znaleziono regułę o tej samej długości, dodaj ją
                    order_data[order]['rules'].add(rule)
            else:
                # Jeśli nie, dodaj nową regułę
                order_data[order] = {'min_length': length, 'rules': set([rule])}

    # Znajdź maksymalną liczbę reguł dla jednego Order
    max_rules = max(len(data['rules']) for data in order_data.values())

    # Tworzenie listy wyników
    result = []
    for order, data in order_data.items():
        row = {'Order': order, 'Length': data['min_length']}
        for i, rule in enumerate(data['rules'], 1):
            row[f'Rule_{i}'] = rule
        # Dodaj puste wartości dla brakujących reguł
        for i in range(len(data['rules']) + 1, max_rules + 1):
            row[f'Rule_{i}'] = ''
        result.append(row)

    # Sortowanie wyników po Order
    result.sort(key=lambda x: x['Order'])

    # Przygotowanie nagłówków
    fieldnames = ['Order', 'Length'] + [f'Rule_{i}' for i in range(1, max_rules + 1)]

    # Zapisanie do pliku CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    print(f"Zapisano zbiorczy plik z najkrótszymi regułami: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/combined_rules/'
output_file = '../RESULTS/shortest_rules_summary.csv'

collect_shortest_rules(input_folder, output_file)

# import pandas as pd
# import os

# # Funkcja do czyszczenia reguł i usuwania duplikatów w wierszu
# def clean_and_deduplicate(row):
#     unique_rules = set()
#     cleaned_row = []
#     for col in row.index:
#         rule = row[col]
#         if isinstance(rule, str):
#             cleaned_rule = rule.strip("(),\"")
#             if cleaned_rule not in unique_rules:
#                 unique_rules.add(cleaned_rule)
#                 cleaned_row.append(cleaned_rule)
#     return cleaned_row

# # Funkcja do usuwania duplikatów w całym DataFrame
# def remove_duplicates_from_dataframe(df):
#     for i, row in df.iterrows():
#         unique_rules = clean_and_deduplicate(row)
#         for j, rule in enumerate(unique_rules):
#             df.at[i, df.columns[j + 1]] = rule  # +1 to skip the 'Row Number' column
#         for j in range(len(unique_rules), len(df.columns) - 1):
#             df.at[i, df.columns[j + 1]] = ""  # Fill the rest with empty strings
#     return df

# base_rules_folder = '../RESULTS/subtable_'
# for i in range(1,6):
# # Wczytanie pliku CSV
#     csv_file = os.path.join(f"../RESULTS/subtable_{i}/6matched_rows{i}.csv")
#     df = pd.read_csv(csv_file)

#     # Usunięcie duplikatów
#     df = remove_duplicates_from_dataframe(df)

#     # Zapisanie wyniku do nowego pliku CSV
#     output_file = os.path.join(f"{base_rules_folder}{i}", f"7matched_rows_unique{i}.csv")
#     df.to_csv(output_file, index=False)

#     print("Usuwanie duplikatów zakończone sukcesem.")


