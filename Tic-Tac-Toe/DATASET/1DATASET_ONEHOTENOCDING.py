import pandas as pd

def apply_one_hot_encoding(dataset):
    encoded_data = pd.DataFrame()
    for column in dataset.columns[:-1]:  # Iteracja po wszystkich kolumnach, z wyjątkiem ostatniej (klasy)
        unique_values = dataset[column].unique()  # Pobranie unikalnych wartości w kolumnie
        for value in unique_values:
            new_column_name = f"{column}-{value}"
            encoded_data[new_column_name] = (dataset[column] == value).astype(int)  # Tworzenie kolumny kodowania one-hot
    encoded_data['Class'] = dataset['Class']  # Dodanie kolumny klasy
    return encoded_data

# Wczytanie danych z pliku CSV
csv_file = "./modified_tic-tac-toe.csv"
df = pd.read_csv(csv_file)

# Usuń wiersz, który zawiera same wartości "c"
df = df[~(df.iloc[:, :-1] == 'c').all(axis=1)]

# Zastosuj one-hot encoding
encoded_df = apply_one_hot_encoding(df)

# Zapisz dane do nowego pliku CSV
encoded_csv_file = "encoded_tic_tac_toe.csv"
encoded_df.to_csv(encoded_csv_file, index=False)

print("Zapisano zaszyfrowane dane do pliku:", encoded_csv_file)
