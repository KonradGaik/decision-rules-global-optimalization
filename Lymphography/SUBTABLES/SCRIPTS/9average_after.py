import csv
import ast

# Funkcja do przetwarzania wiersza
def process_row(row):
    row_number = row[0]
    try:
        matched_rules = ast.literal_eval(row[1])
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing row {row_number}: {e}")
        return []

    unique_rules = set()
    rule_lengths = []

    # Przetwarzanie każdej reguły i dodanie jej do zbioru unikalnych reguł
    for rule in matched_rules:
        try:
            rule_str = rule.strip()
            rule_length = len(rule_str.split('&&'))
            unique_rules.add((rule_str, rule_length))
            rule_lengths.append(rule_length)
        except (ValueError, SyntaxError) as e:
            print(f"Skipping invalid rule format in row {row_number}: {e}")
            continue

    # Tworzenie osobnych wierszy dla każdej unikalnej reguły
    processed_rows = []
    for rule_tuple in unique_rules:
        processed_rows.append([row_number, rule_tuple[0], rule_tuple[1]])

    return processed_rows

# Przetwarzanie plików CSV
for i in range(1, 6):
    input_file = f'./subtable_{i}/5matched_rows_shortest_{i}.csv'
    output_file = f'./subtable_{i}/unique_rows_and_length_shortest_{i}.csv'
    
    with open(input_file, 'r') as file_in, open(output_file, 'w', newline='') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        
        # Pominięcie nagłówka
        next(reader)
        
        # Dodanie nagłówka do pliku wyjściowego
        writer.writerow(['Row Number', 'Rule', 'Rule Length'])
        
        # Przetwarzanie wierszy
        for row in reader:
            processed_rows = process_row(row)
            for processed_row in processed_rows:
                writer.writerow(processed_row)
