import csv

# Nazwa pliku CSV
filename = '../RESULTS/subtable_5/10after_avg5.csv'

# Zbiór do przechowywania unikalnych reguł decyzyjnych
unique_rules = set()

# Czytanie pliku CSV
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Pomijanie nagłówka
    next(csvreader)
    
    # Dodawanie reguł do zbioru unikalnych reguł
    for row in csvreader:
        rule = row[1]
        unique_rules.add(rule)

# Wyświetlanie wszystkich unikalnych reguł decyzyjnych
for rule in unique_rules:
    print(rule)

# Wyświetlanie liczby unikalnych reguł decyzyjnych
print(f'Liczba unikalnych reguł decyzyjnych: {len(unique_rules)}')
