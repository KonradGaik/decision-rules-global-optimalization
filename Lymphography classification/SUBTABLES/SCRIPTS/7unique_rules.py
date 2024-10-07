import os
import pandas as pd
import csv
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import glob

def add_order_column(csv_file):
    output_file = csv_file.replace('.csv', '_ordered.csv')
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Order'] + rows[0])  # Write header with 'Order' as first column
        for idx, row in enumerate(rows[1:], start=1):
            writer.writerow([idx] + row)  # Write each row with its order index

    return output_file

def replace_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if all(value == "c" for value in row):
                continue
            attribute_combination = tuple(row[:-1])
            decision = row[-1]
            decision_grouped[attribute_combination].append(decision)

    # Usuwanie duplikatów decyzji w każdej grupie
    for combination, decisions in decision_grouped.items():
        most_common_decision = max(set(decisions), key=decisions.count)
        decision_grouped[combination] = [most_common_decision]

    return decision_grouped

def save_to_csv_with_order(decision_grouped, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for combination, decisions in decision_grouped.items():
            for decision in decisions:
                row = list(combination) + [decision]
                writer.writerow(row)

def generate_decision_rules(train_data, target):
    # Indukcja drzew decyzyjnych
    X_train = train_data.drop(columns=target)
    y_train = train_data[target]
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    return clf

def classify_test_data(model, test_data, target):
    X_test = test_data.drop(columns=target)
    y_test = test_data[target]
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return predictions, accuracy

def collect_shortest_rules(input_folder, output_file):
    shortest_rules = {}

    # Wzorzec nazwy pliku
    pattern = os.path.join(input_folder, '2consistent_modified_lymphography*.csv')

    for file in sorted(glob.glob(pattern)):
        df = pd.read_csv(file)
        
        for _, row in df.iterrows():
            order = row['Order']
            length = int(row['Rule_Length']) if 'Rule_Length' in row else len(row['Rule'])  # Upewnij się, że kolumna istnieje
            rule = row['Rule']
            
            if order in shortest_rules:
                if length < shortest_rules[order]['min_length']:
                    shortest_rules[order] = {'min_length': length, 'rule': rule}
            else:
                shortest_rules[order] = {'min_length': length, 'rule': rule}

    result = []
    for order, data in shortest_rules.items():
        result.append({'Order': order, 'Shortest_Length': data['min_length'], 'Shortest_Rule': data['rule']})

    result_df = pd.DataFrame(result)
    result_df.to_csv(output_file, index=False)
    print(f"Zapisano najkrótsze reguły do pliku: {output_file}")

# Ensure the output directories exist
for x in range(1, 6):
    output_dir = f'../RESULTS/subtable_{x}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# KROK 1: Utworzenie podtablic z reduktów
df = pd.read_csv('../modified_lymphography.csv')

# Usunięcie wierszy z niespójnymi danymi
df = df[~df.apply(lambda row: all(value == 'c' for value in row), axis=1)]

reducts = [
    {'block_of_affere', 'changes_in_node', 'changes_in_stru', 'special_forms', 'dislocation_of', 'no_of_nodes_in'},
    {'block_of_affere', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'},
    {'block_of_affere', 'changes_in_lym', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_lym', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'}
]

# KROKI 4-8: Podział, indukcja, optymalizacja, klasyfikacja, średnia
results = []

for idx, reduct in enumerate(reducts, start=1):
    df_selected = df[list(reduct) + ['class']]
    output_csv = os.path.join(f'../RESULTS/subtable_{idx}', f'1lymphography_reduct_subtable_{idx}.csv')
    df_selected.to_csv(output_csv, index=False)

    # Dodanie kolumny 'Order'
    output_with_order = add_order_column(output_csv)

    # Usuwanie niespójności i zapis z 'Order'
    decision_grouped = replace_inconsistencies(output_with_order)
    save_to_csv_with_order(decision_grouped, os.path.join(f'../RESULTS/subtable_{idx}', f'2consistent_modified_lymphography{idx}.csv'))

    # Podział na train i test (70/30)
    for _ in range(5):  # Powtórzenie kroków 4-8 pięć razy
        train_data, test_data = train_test_split(df_selected, test_size=0.3)

        # Indukcja drzew
        model = generate_decision_rules(train_data, target='class')

        # Klasyfikacja na danych testowych
        predictions, accuracy = classify_test_data(model, test_data, target='class')

        # Zbieranie wyników
        results.append({
            'subtable': idx,
            'predictions': predictions,
            'accuracy': accuracy
        })

# Zbieranie najkrótszych reguł po zakończeniu procesu
shortest_rules_output_file = '../RESULTS/shortest_rules_summary.csv'
collect_shortest_rules('../RESULTS/subtable_', shortest_rules_output_file)

# Wyświetlenie średniej dokładności dla każdego podtablicy
for result in results:
    print(f"Subtable {result['subtable']}: Accuracy = {result['accuracy']:.2f}")

# Możesz również dodać logikę do obliczenia średniej dokładności przed i po optymalizacji
