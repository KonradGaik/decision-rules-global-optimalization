# Wczytanie danych z pliku
with open("modified_lymphography_reducts", "r") as file:
    data = file.readlines()

# Przetwarzanie danych
reducts = []

for entry in data:
    entry = entry.replace("{", "").replace("}", "").replace(",", "").split()
    reducts.append(set(entry[:-1]))

# Zapisanie danych do pliku txt
with open("reducts.txt", "w") as file:
    for reduct in reducts:
        file.write(", ".join(reduct) + "\n")

print("Zapisano dane do pliku reducts.txt")