import pandas as pd

# Wczytaj pliki CSV
decision_rules_df = pd.read_csv('5decision_rules5.csv')
matched_rows_df = pd.read_csv('6matched_rows5.csv')

# Utwórz pustą ramkę danych
filtered_rules_df = pd.DataFrame()

# Przekształć matched_rows_df do stringa
matched_rows_str = matched_rows_df.to_string()

# Dla każdej reguły w decision_rules_df
for _, rule in decision_rules_df.iterrows():
    # Jeśli reguła jest w matched_rows_df, dodaj ją do filtered_rules_df
    if rule.to_string() in matched_rows_str:
        filtered_rules_df = filtered_rules_df.append(rule)

# Zapisz filtered_rules_df do pliku CSV
filtered_rules_df.to_csv('filtered_rules.csv', index=False)