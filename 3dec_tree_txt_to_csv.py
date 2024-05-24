import csv

# Funkcja do wczytywania reguł decyzyjnych z pliku tekstowego
def read_decision_rules(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Wczytaj reguły decyzyjne z pliku tekstowego


for x in range(1,6):
    decision_rules = read_decision_rules(f'subtable_{x}/3decision_rules_{x}.txt')


    with open(f'subtable_{x}/3decision_rules{x}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for rule in decision_rules:
            condition, class_label = rule.split(', class: ')
            condition = condition.replace('(', '').replace(')', '').replace('&', ',').replace(' ', '')
            writer.writerow([condition, class_label])
        print(f"Reguły decyzyjne zostały zapisane do pliku decision_rules{x}.csv!")
