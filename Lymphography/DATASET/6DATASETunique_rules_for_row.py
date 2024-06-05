import pandas as pd

def count_unique_rules(file_path, inx):
    # Wczytanie danych z pliku CSV
    df = pd.read_csv(file_path)
    
    # Funkcja do zliczania unikalnych reguł
    def unique_rule_count(matched_rules_str):
        try:
            # Podział reguł na pojedyncze elementy
            rules = matched_rules_str.strip('[]').split(', ')
            # Utworzenie zbioru unikalnych reguł
            unique_rules = set(rules)
            return len(unique_rules)
        except Exception as e:
            print(f"Error parsing rules: {e}")
            return 0

    # Zastosowanie funkcji do kolumny "Matched Rules"
    df['Unique Rule Count'] = df['Matched Rules'].apply(unique_rule_count)
    
    # Zapis danych do pliku CSV
    output_file_path = f'./6after_unique_rule_count.csv'
    df.to_csv(output_file_path, index=False)

    # Znalezienie i wydrukowanie najdłuższej reguły
    longest_rule_index = df['Unique Rule Count'].idxmax()
    longest_rule = df.loc[longest_rule_index, 'Matched Rules']
    print(f"Najdłuższa reguła decyzyjna dla podtabeli {inx}: {longest_rule}")

    return output_file_path

i = ''
file_path = f'./5matched_rows_shortest.csv'
output_file = count_unique_rules(file_path, i)
print(f"Wynik zapisano do: {output_file}")
