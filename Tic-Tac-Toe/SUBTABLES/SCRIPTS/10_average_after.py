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

    # Obliczanie średniej długości reguł
    total_length = 0
    rule_count = 0
    for rule in matched_rules:
        try:
            if isinstance(rule, dict) and 'Rule' in rule:
                rule_str = rule['Rule'].strip()
            else:
                rule_str = rule.strip()
            rule_length = len(rule_str.split('&&'))
            total_length += rule_length
            rule_count += 1
        except (ValueError, SyntaxError) as e:
            print(f"Skipping invalid rule format in row {row_number}: {e}")
            continue

    average_rule_length = total_length / rule_count if rule_count > 0 else 0

    # Tworzenie wiersza z numerem wiersza, regułami i średnią długością
    processed_rows = [[row_number, f"{average_rule_length:.1f}".replace('.', ',')]]

    return processed_rows

# Przetwarzanie plików CSV
for i in range(1, 6):
    input_file = f'../RESULTS/subtable_{i}/8_optimized_rules{i}.csv'
    output_file = f'../RESULTS/subtable_{i}/10after_avg{i}.csv'
    
    with open(input_file, 'r') as file_in, open(output_file, 'w', newline='') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        
        # Pominięcie nagłówka
        next(reader)
        
        # Dodanie nagłówka do pliku wyjściowego
        writer.writerow(['Row Number', 'Average Rule Length'])
        
        # Przetwarzanie wierszy
        for row in reader:
            processed_rows = process_row(row)
            for processed_row in processed_rows:
                writer.writerow(processed_row)


# import csv
# import ast

# # Funkcja do przetwarzania wiersza
# def process_row(row):
#     row_number = row[0]
#     try:
#         matched_rules = ast.literal_eval(row[1])
#     except (ValueError, SyntaxError) as e:
#         print(f"Error parsing row {row_number}: {e}")
#         return []

#     unique_rules = set()
#     shortest_rule_length = float('inf')

#     # Przetwarzanie każdej reguły i dodanie jej do zbioru unikalnych reguł
#     for rule in matched_rules:
#         try:
#             rule_str = rule.strip()
#             if '=>' in rule_str:
#                 rule_str, _ = rule_str.split('=>')
#             if '&& negative' in rule_str:
#                 rule_str = rule_str.replace('&& negative', '')
#             elif '&& positive' in rule_str:
#                 rule_str = rule_str.replace('&& positive', '')
#             rule_length = len(rule_str.split('&&'))
#             if rule_length < shortest_rule_length:
#                 unique_rules = set()  # Czyszczenie zbioru unikalnych reguł, jeśli znaleziono krótszą regułę
#                 shortest_rule_length = rule_length
#             if rule_length == shortest_rule_length:
#                 unique_rules.add(rule_str)
#         except (ValueError, SyntaxError) as e:
#             print(f"Skipping invalid rule format in row {row_number}: {e}")
#             continue

#     # Tworzenie osobnych wierszy dla każdej unikalnej reguły
#     processed_rows = []
#     for rule_str in unique_rules:
#         processed_rows.append([row_number, rule_str, shortest_rule_length])

#     return processed_rows

# # Przetwarzanie plików CSV
# for i in range(1, 6):
#     input_file = f'../RESULTS/subtable_{i}/8matched_rows_shortest_{i}.csv'
#     output_file = f'../RESULTS/subtable_{i}/10after_avg_{i}.csv'
    
#     with open(input_file, 'r') as file_in, open(output_file, 'w', newline='') as file_out:
#         reader = csv.reader(file_in)
#         writer = csv.writer(file_out)
        
#         # Pominięcie nagłówka
#         next(reader)
        
#         # Dodanie nagłówka do pliku wyjściowego
#         writer.writerow(['Row Number', 'Rule', 'Rule Length'])
        
#         # Przetwarzanie wierszy
#         for row in reader:
#             processed_rows = process_row(row)
#             for processed_row in processed_rows:
#                 writer.writerow(processed_row)
