

import os
import pandas as pd
import glob
import csv

def collect_order_lengths_and_rules(input_folder, output_file):
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
            length = int(row['Rule_Length'])  # Konwersja na int
            rule = row['Rule']
            
            # Jeśli Order już istnieje w słowniku, dodaj długość i regułę do list
            if order in order_data:
                order_data[order]['lengths'].append(length)
                order_data[order]['rules'].append(rule)
            else:
                # Jeśli nie, utwórz nowe listy z tą długością i regułą
                order_data[order] = {'lengths': [length], 'rules': [rule]}

    # Tworzenie listy wyników
    result = []
    max_length = max(len(data['lengths']) for data in order_data.values())
    
    for order, data in order_data.items():
        row = {'Order': order}
        for i in range(max_length):
            if i < len(data['lengths']):
                row[f'Length_{i+1}'] = data['lengths'][i]
                row[f'Rule_{i+1}'] = data['rules'][i]
            else:
                row[f'Length_{i+1}'] = ''
                row[f'Rule_{i+1}'] = ''
        result.append(row)

    # Sortowanie wyników po Order
    result.sort(key=lambda x: x['Order'])

    # Zapisanie do pliku CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Order'] + [f'Length_{i+1}' for i in range(max_length)] + [f'Rule_{i+1}' for i in range(max_length)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    print(f"Zapisano zbiorczy plik: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/combined_rules/'
output_file = '../RESULTS/order_lengths_and_rules_summary.csv'

collect_order_lengths_and_rules(input_folder, output_file)