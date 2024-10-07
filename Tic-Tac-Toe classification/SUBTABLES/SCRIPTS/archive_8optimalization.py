import pandas as pd

def generate_shortest_rules():
    all_rules = []  # Lista do przechowywania wszystkich reguł

    # Iteracja przez wszystkie subtables
    for subtable_index in range(1, 6):
        # Wczytaj podtablicę z pliku CSV
        subtable_file = f'../RESULTS/subtable_{subtable_index}/train_set_{subtable_index}.csv'
        df = pd.read_csv(subtable_file)

        # Generowanie reguł
        for index, row in df.iterrows():
            rule_conditions = []  # Lista do przechowywania warunków reguły
            
            # Tworzenie warunków reguły na podstawie wartości kolumn
            for col in df.columns:
                if col != 'Order' and col != 'Class':  # Pomijamy kolumny Order i Class
                    rule_conditions.append(f"({col} <= {row[col]})")

            rule_str = ' & '.join(rule_conditions)  # Tworzenie ciągu reguły
            rule_length = len(rule_conditions)  # Długość reguły
            
            # Przechowuj regułę, klasę, i długość w słowniku
            rule_dict = {
                'Rule': rule_str,
                'class': row['Class'],
                'Length': rule_length
            }
            
            all_rules.append(rule_dict)

    # Przekształcenie listy reguł w DataFrame
    rules_df = pd.DataFrame(all_rules)

    # Sortowanie według kolumny 'Length' (opcjonalne)
    rules_df.sort_values(by='Length', inplace=True)

    # Zapisz reguły do pliku CSV
    output_file = '../RESULTS/shortest_rules_with_length.csv'
    rules_df.to_csv(output_file, index=False)

    print(f'Zapisano reguły do {output_file}.')

# Uruchom funkcję
generate_shortest_rules()
