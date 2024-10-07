import pandas as pd

def extract_unique_rules(file_path, output_file_path):
    # Załaduj plik CSV
    df = pd.read_csv(file_path)
    
    # Zbiór do przechowywania unikalnych reguł
    unique_rules_set = set()

    # Funkcja do wyodrębniania reguł
    def extract_rules(matched_rules_str):
        try:
            # Usunięcie nawiasów i podzielenie na reguły po ', '
            rules = matched_rules_str.strip('[]').split(', ')
            # Dodanie reguł do zbioru unikalnych reguł
            for rule in rules:
                unique_rules_set.add(rule.strip("'"))
        except Exception as e:
            print(f"Error parsing rules: {e}")

    # Zastosowanie funkcji do kolumny "Matched Rules"
    df['Matched Rules'].apply(extract_rules)

    # Konwersja zbioru na listę i zapis do nowego pliku CSV
    unique_rules_list = list(unique_rules_set)
    unique_rules_df = pd.DataFrame(unique_rules_list, columns=['Unique Rules'])
    unique_rules_df.to_csv(output_file_path, index=False)

    # Wyświetlenie liczby unikalnych reguł
    print(f"Ogólna liczba unikalnych reguł: {len(unique_rules_list)}")
    print(f"Unikalne reguły zapisano do: {output_file_path}")

for i in range(1,6):
# Ścieżka do pliku wejściowego i wyjściowego
    input_file_path = f'../RESULTS/subtable_{i}/6before_unique_rule_count_{i}.csv'
    output_file_path = f'../RESULTS/subtable_{i}/7unique_rules_output{i}.csv'
    # Wywołanie funkcji
    extract_unique_rules(input_file_path, output_file_path)
