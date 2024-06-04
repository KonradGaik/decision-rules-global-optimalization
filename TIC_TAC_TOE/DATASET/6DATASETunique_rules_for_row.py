import pandas as pd

def count_unique_rules(file_path, inx):
    # Załaduj plik CSV
    df = pd.read_csv(file_path)
    
    # Funkcja do parsowania i liczenia unikalnych reguł
    def unique_rule_count(matched_rules_str):
        try:
            # Usunięcie nawiasów i podzielenie na reguły po ', '
            rules = matched_rules_str.strip('[]').split(', ')
            # Utworzenie zbioru unikalnych reguł
            unique_rules = set(rules)
            return len(unique_rules)
        except Exception as e:
            print(f"Error parsing rules: {e}")
            return 0

    # Zastosowanie funkcji do kolumny "Matched Rules"
    df['Unique Rule Count'] = df['Matched Rules'].apply(unique_rule_count)
    
    # Zapisz wynik do nowego pliku CSV
    output_file_path = (f'./unique_rule_count.csv')
    df.to_csv(output_file_path, index=False)
    return output_file_path
i = ''
file_path = f'./5matched_rows_shortest.csv'
output_file = count_unique_rules(file_path, i)
print(f"Wynik zapisano do: {output_file}")
