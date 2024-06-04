import pandas as pd

def count_unique_rules(file_path, inx):
    # Wczytanie danych z pliku CSV
    df = pd.read_csv(file_path)
    
    # Funkcja do zliczania unikalnych reguł
    def unique_rule_count(matched_rules_str):
        try:
            # Podział reguł na pojedyncze elementy
            rules = matched_rules_str.strip('[]').split(', ')
            # Znalezienie długości najdłuższej reguły
            longest_rule_length = max(len(rule.split(' && ')) for rule in rules)
            return longest_rule_length
        except Exception as e:
            print(f"Error parsing rules: {e}")
            return 0

    # Zastosowanie funkcji do kolumny "Matched Rules"
    df['Longest Rule Length'] = df['Matched Rules'].apply(unique_rule_count)
    
    # Zapis danych do pliku CSV
    output_file_path = f'./subtable_{inx}/6before_unique_rule_count_{inx}.csv'
    df.to_csv(output_file_path, index=False)

    # Znalezienie i wydrukowanie najdłuższej reguły
    longest_rule_index = df['Longest Rule Length'].idxmax()
    longest_rule = df.loc[longest_rule_index, 'Matched Rules']
    print(f"Najdłuższa reguła decyzyjna dla podtabeli {inx}: {longest_rule}")

    return output_file_path

# Dla każdej podtabeli od 1 do 5 wykonaj funkcję count_unique_rules
for i in range(1, 6):
    file_path = f'./subtable_{i}/4matched_rows_{i}.csv'
    output_file = count_unique_rules(file_path, i)
    print(f"Wynik zapisano do: {output_file}")
