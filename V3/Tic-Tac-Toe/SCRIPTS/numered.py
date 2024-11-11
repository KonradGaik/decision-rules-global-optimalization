import pandas as pd

def add_row_numbers_skip_first(input_file, output_file):
    # Wczytanie pliku CSV, pomijając pierwszy wiersz
    df = pd.read_csv(input_file, skiprows=1)
    
    # Dodanie kolumny z numerami wierszy, zaczynając od 1
    df.insert(0, 'Row_Number', range(1, len(df) + 1))
    
    # Zapisanie pliku z nową kolumną numerów wierszy
    df.to_csv(output_file, index=False)
    print(f"Zaktualizowany plik został zapisany jako {output_file}")

# Ścieżki do plików
input_file = '../modified_tic-tac-toe.csv'
output_file = '../modified_tic_tac_toe_with_row_numbers.csv'

# Dodanie numeracji do wierszy, pomijając pierwszy
add_row_numbers_skip_first(input_file, output_file)
