import csv

# Funkcja do wczytywania reguł decyzyjnych z pliku tekstowego
def read_decision_rules(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Funkcja do określenia maksymalnej liczby warunków w regułach
def max_conditions_length(rules):
    max_length = 0
    for rule in rules:
        conditions, _ = rule.split(', class: ')
        conditions = conditions.split('&')
        length = len(conditions)
        if length > max_length:
            max_length = length
    return max_length

# Wczytaj reguły decyzyjne z pliku tekstowego i określ maksymalną liczbę warunków
max_rule_length = 0
for x in range(1, 6):
    decision_rules = read_decision_rules(f'subtable_{x}/3decision_rules_{x}.txt')
    max_rule_length = max(max_rule_length, max_conditions_length(decision_rules))

# Utwórz listę nazw kolumn, uwzględniając maksymalną liczbę warunków
column_names = [f"condition_{i}" for i in range(1, max_rule_length + 1)] + ["class_label"]

# Wczytaj reguły decyzyjne z pliku tekstowego
for x in range(1, 6):
    decision_rules = read_decision_rules(f'subtable_{x}/3decision_rules_{x}.txt')

    with open(f'subtable_{x}/3decision_rules{x}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        for rule in decision_rules:
            conditions, class_label = rule.split(', class: ')
            conditions = conditions.split('&')
            conditions = [c.strip().replace('(', '').replace(')', '') for c in conditions]
            conditions.extend([''] * (max_rule_length - len(conditions)))  # Uzupełnij puste kolumny
            row = conditions + [class_label]
            writer.writerow(row)
        print(f"Reguły decyzyjne zostały zapisane do pliku decision_rules{x}.csv!")
