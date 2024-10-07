import os
import pandas as pd
import glob

def apply_one_hot_encoding(dataset):
    encoded_data = pd.DataFrame()
    for column in dataset.columns[:-1]:  # Iteracja po wszystkich kolumnach, z wyjątkiem ostatniej (klasy)
        unique_values = dataset[column].unique()  # Pobranie unikalnych wartości w kolumnie
        for value in unique_values:
            new_column_name = f"{column}-{value}"
            encoded_data[new_column_name] = (dataset[column] == value).astype(int)  # Tworzenie kolumny kodowania one-hot
    encoded_data['Class'] = dataset['Class']  # Dodanie kolumny klasy
    return encoded_data

def process_and_encode_csv_files():
    for i in range(1, 6):
        # Wczytanie danych z pliku CSV
        csv_file = f"../RESULTS/subtable_{i}/1tic_tac_toe_reduct_subtable_{i}.csv"
        df = pd.read_csv(csv_file)

        # Usuń wiersz, który zawiera same wartości "c"
        df = df[~(df.iloc[:, :-1] == 'c').all(axis=1)]

        # Zastosuj one-hot encoding
        encoded_df = apply_one_hot_encoding(df)

        # Dodanie kolumny Order z numerem porządkowym
        encoded_df.insert(0, 'Order', range(1, len(encoded_df) + 1))

        # Zapisz dane do nowego pliku CSV
        encoded_csv_file = f"../RESULTS/subtable_{i}/3encoded_tic_tac_toe_{i}.csv"
        encoded_df.to_csv(encoded_csv_file, index=False)

        print("Zapisano zaszyfrowane dane do pliku:", encoded_csv_file)

def collect_order_and_lengths(input_folder, output_folder):
    data = {}

    # Wzorzec nazwy pliku
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iteracja po wszystkich pasujących plikach
    for file in sorted(glob.glob(pattern)):
        # Wczytanie pliku CSV
        df = pd.read_csv(file)

        # Grupowanie po Order i zbieranie wszystkich długości
        grouped = df.groupby('Order')['Rule_Length'].apply(list)

        # Dodanie długości do słownika data
        for order, lengths in grouped.items():
            if order in data:
                data[order].extend(lengths)
            else:
                data[order] = lengths

    # Debug: Print the collected data
    print(f"Collected data: {data}")

    # Safeguard against empty data
    if not data:
        print("No data collected. Exiting the function.")
        return  # Or handle as needed

    # Tworzenie i zapisywanie pliku CSV
    result = []
    max_lengths = max(len(lengths) for lengths in data.values())
    
    for order, lengths in data.items():
        row = {'Order': order}
        for i in range(max_lengths):
            if i < len(lengths):
                row[f'Length_{i+1}'] = lengths[i]
            else:
                row[f'Length_{i+1}'] = None  # lub możesz użyć 0 zamiast None
        result.append(row)

    # Konwersja listy słowników na DataFrame
    result_df = pd.DataFrame(result)

    # Sortowanie wyników po Order
    result_df = result_df.sort_values('Order')

    # Zapisanie do pliku CSV
    output_file = os.path.join(output_folder, 'order_and_lengths_summary.csv')
    result_df.to_csv(output_file, index=False)
    print(f"Zapisano plik: {output_file}")

# Użycie funkcji
input_folder = '../RESULTS/rules_output/'
output_folder = '../RESULTS/'

# Upewnij się, że folder wyjściowy istnieje
os.makedirs(output_folder, exist_ok=True)

# Przetwarzanie plików i kodowanie one-hot
process_and_encode_csv_files()

# Zbieranie Order i Rule_Length z plików rule_*.csv
collect_order_and_lengths(input_folder, output_folder)
