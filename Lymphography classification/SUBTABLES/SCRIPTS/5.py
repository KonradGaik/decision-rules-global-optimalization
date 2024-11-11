# optimize_rules.py
import pandas as pd

def optimize_rules(rules_file, output_file):
    with open(rules_file, 'r') as f:
        rules = f.readlines()
    optimized_rules = sorted(rules, key=lambda x: len(x.split()))  # Sortowanie wg długości
    with open(output_file, 'w') as f:
        f.writelines(optimized_rules)
    print("Reguły zoptymalizowane względem długości:", output_file)

# Użycie
for i in range(1, 6):
    rules_file = f"../RESULTS/subtable_{i}/rules.txt"
    output_file = f"../RESULTS/subtable_{i}/optimized_rules.txt"
    optimize_rules(rules_file, output_file)
