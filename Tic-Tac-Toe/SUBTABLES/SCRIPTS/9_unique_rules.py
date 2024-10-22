import csv

unique_rules = set()

with open('../RESULTS/shortest_rules_summary.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        for i in range(1, 5):  # Sprawdzamy Rule_1 do Rule_4
            rule = row.get(f'Rule_{i}')
            if rule and rule.strip():  # Jeśli reguła nie jest pusta
                unique_rules.add(rule.strip())

print(f"Liczba unikalnych reguł: {len(unique_rules)}")