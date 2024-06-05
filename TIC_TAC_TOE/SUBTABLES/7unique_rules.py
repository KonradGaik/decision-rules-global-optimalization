import pandas as pd


def count_unique_rules(csv_file):
    # Wczytanie pliku CSV
    df = pd.read_csv(csv_file, header=None, names=['Row', 'Matched Rules'])
    
    # Wyodrębnienie kolumny z regułami i usunięcie ewentualnych białych znaków
    df['Matched Rules'] = df['Matched Rules'].str.strip()
    
    # Usunięcie duplikatów
    unique_rules = df.drop_duplicates(subset='Matched Rules', keep=False)['Matched Rules']
    
    # Zwrócenie liczby unikalnych reguł i samej serii unikalnych reguł
    return len(unique_rules), unique_rules
for i in range(1,6):
    # Podaj ścieżkę do swojego pliku CSV
    csv_file_path =  f'./subtable_{i}/matched_rows_shortest_{i}.csv'

    # Policz unikalne reguły i wyświetl je
    unique_rule_count, unique_rules = count_unique_rules(csv_file_path)
    print(f'zbior {i}')
    print(f"Liczba unikalnych reguł występujących tylko raz: {unique_rule_count}")
    print("Unikalne reguły:")
    #print(unique_rules.to_string(index=False))
