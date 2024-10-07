import csv
from collections import defaultdict
import os
import pandas as pd

# Funkcja do usuwania niespójności
def remove_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    header = None  # Initialize header variable
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        header_without_order = header[1:]  # Remove the first column
        
        for row in reader:
            attributes = tuple(row[1:])  # All columns except the first one
            order = row[0]  # First column (Order)
            decision_grouped[attributes].append(order)
    
    # Remove inconsistencies and keep the most common order value for each attribute combination
    cleaned_data = {}
    for attributes, orders in decision_grouped.items():
        if len(set(orders)) == 1:
            cleaned_data[attributes] = orders[0]  # Only one unique order, keep it
        else:
            most_common_order = max(set(orders), key=orders.count)
            cleaned_data[attributes] = most_common_order
    
    return cleaned_data, header_without_order  # Return cleaned data and header without the first column

# Funkcja do zapisywania wyczyszczonych danych
def save_cleaned_data(cleaned_data, header, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)
    
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        for attributes, order in cleaned_data.items():
            row = [order] + list(attributes)
            writer.writerow(row)

# Funkcja do kodowania one-hot
def apply_one_hot_encoding(dataset):
    encoded_data = pd.get_dummies(dataset.drop('Class', axis=1))
    encoded_data['Class'] = dataset['Class']  # Dodanie kolumny klasy na końcu
    return encoded_data

# Funkcja do przetwarzania i kodowania plików CSV
def process_and_encode_csv_files(input_csv, output_folder, output_file):
    # Wczytanie danych z pliku CSV
    df = pd.read_csv(input_csv)
    
    # Usuń wiersz, który zawiera same wartości "c"
    df = df[~(df.iloc[:, :-1] == 'c').all(axis=1)]
    
    # Usuwanie niespójności
    cleaned_data, header = remove_inconsistencies(input_csv)
    
    # Zapisz wyczyszczone dane
    save_cleaned_data(cleaned_data, header, output_folder, f"cleaned_{output_file}")
    
    # Wczytaj ponownie dane po usunięciu niespójności
    cleaned_df = pd.read_csv(os.path.join(output_folder, f"cleaned_{output_file}"))
    
    # Zastosuj one-hot encoding
    encoded_df = apply_one_hot_encoding(cleaned_df)
    
    # Dodanie kolumny Order z numerem porządkowym
    encoded_df.insert(0, 'Order', range(1, len(encoded_df) + 1))
    
    # Zapisz zakodowane dane do nowego pliku CSV
    encoded_csv_file = os.path.join(output_folder, f"encoded_{output_file}")
    encoded_df.to_csv(encoded_csv_file, index=False)
    
    print(f"Zapisano zakodowane dane do pliku: {encoded_csv_file}")

# Przetwarzanie subtabel Lymphography
for i in range(1, 6):
    input_csv = f"../RESULTS/subtable_{i}/1lymphography_reduct_subtable_{i}.csv"
    output_folder = f"../RESULTS/subtable_{i}"
    output_file = f"lymphography_{i}.csv"
    
    process_and_encode_csv_files(input_csv, output_folder, output_file)
