# import pandas as pd
# import ast

# def extract_unique_rules(input_file, output_file):
#     # Wczytanie danych
#     data = pd.read_csv(input_file)

#     # Inicjalizacja zbioru do przechowywania unikalnych reguł
#     unique_rules = set()

#     # Iteracja po wierszach danych
#     for row in data['Shortest Rules']:
#         # Konwersja łańcucha znaków do listy słowników
#         rules = ast.literal_eval(row)
#         for rule_dict in rules:
#             # Dodanie reguły do zbioru unikalnych reguł
#             unique_rules.add(rule_dict['Rule'])

#     # Konwersja zbioru unikalnych reguł do listy i utworzenie DataFrame
#     unique_rules_df = pd.DataFrame(list(unique_rules), columns=['Unique Rules'])
#     unique_rules_df = unique_rules_df.drop_duplicates()
#     # Zapisanie unikalnych reguł do pliku CSV
#     unique_rules_df.to_csv(output_file, index=False)

#     print(f"Unikalne reguły zostały zapisane do pliku {output_file}")

# for i in range(1, 6):
#     input_file = f'../RESULTS/subtable_{i}/8matched_rows_shortest_{i}.csv'
#     output_file = f'../RESULTS/subtable_{i}/11unique_rules{i}.csv'
#     extract_unique_rules(input_file, output_file)