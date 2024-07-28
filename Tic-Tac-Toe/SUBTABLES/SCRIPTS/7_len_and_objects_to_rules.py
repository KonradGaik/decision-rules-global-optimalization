
import os
import pandas as pd
import glob

def collect_order_and_lengths(input_folder, output_folder):
    subtable_data = {i: {} for i in range(1, 6)}

    # Wzorzec nazwy pliku
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iteracja po wszystkich pasujących plikach
    for file in sorted(glob.glob(pattern)):
        # Wyodrębnienie indeksu podtablicy z nazwy pliku
        subtable_index = int(os.path.basename(file).split('_')[1])
        
        # Wczytanie pliku CSV
        df = pd.read_csv(file)
        
        # Grupowanie po Order i zbieranie wszystkich długości
        grouped = df.groupby('Order')['Rule_Length'].apply(list)
        
        # Dodanie długości do odpowiedniej podtablicy
        for order, lengths in grouped.items():
            if order in subtable_data[subtable_index]:
                subtable_data[subtable_index][order].extend(lengths)
            else:
                subtable_data[subtable_index][order] = lengths

    # Tworzenie i zapisywanie plików CSV dla każdej podtablicy
    for subtable_index, data in subtable_data.items():
        result = []
        max_lengths = max(len(lengths) for lengths in data.values())
        
        for order, lengths in data.items():
            row = {'Order': order}
            for i in range(max_lengths):
                if i < len(lengths):
                    row[f'Length_{i+1}'] = lengths[i]
                else:
                    row[f'Length_{i+1}'] = None
            result.append(row)

        # Konwersja listy słowników na DataFrame
        result_df = pd.DataFrame(result)

        # Sortowanie wyników po Order
        result_df = result_df.sort_values('Order')

        # Zapisanie do pliku CSV
        output_file = os.path.join(output_folder, f'order_and_lengths_subtable_{subtable_index}.csv')
        result_df.to_csv(output_file, index=False)
        print(f"Zapisano plik dla podtablicy {subtable_index}: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/combined_rules/'
output_folder = '../RESULTS/order_and_lengths_summaries/'

# Upewnij się, że folder wyjściowy istnieje
os.makedirs(output_folder, exist_ok=True)

collect_order_and_lengths(input_folder, output_folder)

# import os
# import pandas as pd
# import ast

# def process_files(base_rules_folder):
#     for i in range(1, 6):
#         csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"7matched_rows_unique{i}.csv")
#         data_df = pd.read_csv(csv_file_data)
#         shortest_rules_df = match_rules_to_rows(data_df)
#         shortest_rules_df.to_csv(os.path.join(f"{base_rules_folder}{i}", f"8matched_rows_shortest_{i}.csv"), index=False)

# def match_rules_to_rows(data_df):
#     matched_rows = []
#     for i, row in data_df.iterrows():
#         row_number = i + 1  
#         matched_rules = ast.literal_eval(row['Matched Rules'])
#         shortest_rule_length = min(len(rule['Rule'].split('&&')) for rule in matched_rules)
#         shortest_rules = [rule for rule in matched_rules if len(rule['Rule'].split('&&')) == shortest_rule_length]
#         matched_rows.append({'Row Number': row_number, 'Shortest Rules': shortest_rules})
#     matched_rows_df = pd.DataFrame(matched_rows)
#     return matched_rows_df

# if __name__ == "__main__":
#     base_rules_folder = '../RESULTS/subtable_'
#     process_files(base_rules_folder)