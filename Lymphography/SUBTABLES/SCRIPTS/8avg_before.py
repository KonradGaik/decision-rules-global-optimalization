import pandas as pd

# Funkcja do obliczania liczby warunków w regule
def count_conditions(rule):
    return rule.count('&&') + 1

# Funkcja do obliczania średniej długości reguł w wierszu, zaokrąglonej do liczby całkowitej i zamiany kropki na przecinek
def average_rule_length(rules):
    rules_list = [rule.strip() for rule in rules.split(",")]
    lengths = [count_conditions(rule.split("=>")[0]) for rule in rules_list]
    average_length = (sum(lengths) / len(lengths))
    return str(average_length).replace('.', ',')

for i in range(1,6):
# Odczytaj plik CSV
    input_file = f'../RESULTS/subtable_{i}/6matched_rows_optimalizated_{i}.csv'
    df = pd.read_csv(input_file)

    # Oblicz średnią długość reguł dla każdego wiersza
    df['Average Rule Length'] = df['Matched Rules'].apply(average_rule_length)

    # Zapisz wynik do nowego pliku CSV
    output_file = f'../RESULTS/subtable_{i}/8average_rule_length_before{i}.csv'
    df[['Row Number', 'Average Rule Length']].to_csv(output_file, index=False)

    print(f"Średnia długość reguł została zapisana do pliku {output_file}.")



