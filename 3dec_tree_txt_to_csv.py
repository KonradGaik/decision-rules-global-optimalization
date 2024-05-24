import csv
import re

# Funkcja do parsowania wierszy z pliku tekstowego
def parse_line(line, attributes):
    parts = line.strip().split(", class: ")
    class_label = parts[1]
    conditions = parts[0].split(") & (")
    conditions[0] = conditions[0][1:]  # Usunięcie początkowego nawiasu '('
    conditions[-1] = conditions[-1][:-1]  # Usunięcie końcowego nawiasu ')'
    
    condition_dict = {attr: "" for attr in attributes}
    condition_dict["class"] = class_label
    for condition in conditions:
        for key in condition_dict.keys():
            if key in condition:
                condition_dict[key] = condition.strip()
                break
    
    return condition_dict

# Wczytanie pliku tekstowego i przetworzenie jego zawartości
input_file = "subtable_1/3decision_rules_1.txt"
output_file = "output.csv"

with open(input_file, "r") as file:
    lines = file.readlines()

# Ekstrakcja wszystkich unikalnych atrybutów
attribute_set = set()
for line in lines:
    parts = line.strip().split(", class: ")[0]
    conditions = parts.split(") & (")
    conditions[0] = conditions[0][1:]  # Usunięcie początkowego nawiasu '('
    conditions[-1] = conditions[-1][:-1]  # Usunięcie końcowego nawiasu ')'
    
    for condition in conditions:
        attr_name = condition.split(" ")[0]
        attribute_set.add(attr_name)

attributes = list(attribute_set)
attributes.sort()  # Sortowanie atrybutów dla uporządkowanego CSV
attributes.append("class")

parsed_lines = [parse_line(line, attributes) for line in lines]

# Zapisanie wyników do pliku CSV
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=attributes)
    
    writer.writeheader()
    for parsed_line in parsed_lines:
        writer.writerow(parsed_line)

print(f"Plik CSV został wygenerowany: {output_file}")
