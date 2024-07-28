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