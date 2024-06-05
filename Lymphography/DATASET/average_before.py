import csv

# Funkcja do przetwarzania wiersza
def process_row(row):
    row_number = row[0]
    matched_rules = row[1].split("}, ")
    unique_rules = set()
    
    # Przetwarzanie każdej reguły i dodanie jej do zbioru unikalnych reguł
    for rule in matched_rules:
        rule_str = rule.split("'Rule': ")[-1].strip("'")
        rule_length = rule.split("'Rule Length': ")[-1].strip("},)")
        unique_rules.add((rule_str, rule_length))

    # Tworzenie osobnych wierszy dla każdej unikalnej reguły
    processed_rows = []
    for rule_tuple in unique_rules:
        processed_rows.append([row_number, rule_tuple[0], rule_tuple[1]])

    return processed_rows

# Otwórz plik CSV wejściowy i utwórz plik CSV wyjściowy
with open('4matched_rows.csv', 'r') as file_in, open('przetworzone_dane.csv', 'w', newline='') as file_out:
    reader = csv.reader(file_in)
    writer = csv.writer(file_out)

    # Przetwarzanie wierszy
    for row in reader:
        processed_rows = process_row(row)
        for processed_row in processed_rows:
            writer.writerow(processed_row)
