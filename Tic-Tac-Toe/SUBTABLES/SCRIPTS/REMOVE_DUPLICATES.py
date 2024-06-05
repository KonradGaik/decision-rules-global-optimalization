import csv
import ast

# Funkcja do przetwarzania wiersza
def process_row(row):
    row_number = row[0]
    matched_rules_str = row[1].strip('"[]')
    matched_rules = matched_rules_str.split("}, ")
    
    unique_rules = set()

    # Przetwarzanie każdej reguły i dodanie jej do zbioru unikalnych reguł
    for rule in matched_rules:
        if rule[-1] != '}':
            rule += '}'
        try:
            rule_dict = ast.literal_eval(rule)
            rule_str = rule_dict['Rule']
            rule_length = rule_dict['Rule Length']
            unique_rules.add((rule_str, rule_length))
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing rule: {rule} - {e}")
            continue

    # Tworzenie osobnych wierszy dla każdej unikalnej reguły
    processed_rows = []
    for rule_tuple in unique_rules:
        processed_rows.append([row_number, rule_tuple[0], rule_tuple[1]])

    return processed_rows

# Otwórz plik CSV wejściowy i utwórz plik CSV wyjściowy
with open('./matched_rows.csv', 'r') as file_in, open('output.csv', 'w', newline='') as file_out:
    reader = csv.reader(file_in)
    writer = csv.writer(file_out)

    # Zapisz nagłówki
    headers = next(reader)
    writer.writerow(headers[:2] + ["Rule", "Rule Length"])

    # Przetwarzanie wierszy
    for row in reader:
        processed_rows = process_row(row)
        for processed_row in processed_rows:
            writer.writerow(processed_row)
