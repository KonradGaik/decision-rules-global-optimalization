import pandas as pd
import os
# Sprawdź czy nie usuwa nieduplikatow TODO
# Funkcja do czyszczenia reguł i usuwania duplikatów w wierszu
def clean_and_deduplicate(row):
    unique_rules = set()
    cleaned_row = []
    for col in row.index:
        rule = row[col]
        if isinstance(rule, str):
            cleaned_rule = rule.strip("(),\"")
            if cleaned_rule not in unique_rules:
                unique_rules.add(cleaned_rule)
                cleaned_row.append(cleaned_rule)
    return cleaned_row

# Funkcja do usuwania duplikatów w całym DataFrame
def remove_duplicates_from_dataframe(df):
    for i, row in df.iterrows():
        unique_rules = clean_and_deduplicate(row)
        for j, rule in enumerate(unique_rules):
            df.at[i, df.columns[j + 1]] = rule  # +1 to skip the 'Row Number' column
        for j in range(len(unique_rules), len(df.columns) - 1):
            df.at[i, df.columns[j + 1]] = ""  # Fill the rest with empty strings
    return df

# Wczytanie pliku CSV
csv_file = os.path.join(f"../RESULTS", f"4matched_rows.csv")
df = pd.read_csv(csv_file)

# Usunięcie duplikatów
df = remove_duplicates_from_dataframe(df)

# Zapisanie wyniku do nowego pliku CSV
output_file = os.path.join(f"../RESULTS", f"5matched_rows_unique.csv")
df.to_csv(output_file, index=False)

print("Usuwanie duplikatów zakończone sukcesem.")
