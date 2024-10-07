import csv
from collections import defaultdict
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import glob

# Funkcja do usuwania niespójności
def remove_inconsistencies(csv_file):
    decision_grouped = defaultdict(list)
    header = None
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        header_without_order = header[1:]
        
        for row in reader:
            attributes = tuple(row[1:])
            order = row[0]
            decision_grouped[attributes].append(order)
    
    cleaned_data = {}
    for attributes, orders in decision_grouped.items():
        if len(set(orders)) == 1:
            cleaned_data[attributes] = orders[0]
        else:
            most_common_order = max(set(orders), key=orders.count)
            cleaned_data[attributes] = most_common_order
    
    return cleaned_data, header_without_order

# Funkcja do zapisywania wyczyszczonych danych
def save_cleaned_data(cleaned_data, header, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)
    
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for attributes, order in cleaned_data.items():
            row = [order] + list(attributes)
            writer.writerow(row)

# Funkcja do kodowania one-hot
def apply_one_hot_encoding(dataset):
    encoded_data = pd.get_dummies(dataset.drop('Class', axis=1))
    encoded_data['Class'] = dataset['Class']
    return encoded_data

# Funkcja do przetwarzania i kodowania plików CSV
def process_and_encode_csv_files(input_csv, output_folder, output_file):
    df = pd.read_csv(input_csv)
    df = df[~(df.iloc[:, :-1] == 'c').all(axis=1)]
    
    cleaned_data, header = remove_inconsistencies(input_csv)
    save_cleaned_data(cleaned_data, header, output_folder, f"cleaned_{output_file}")
    
    cleaned_df = pd.read_csv(os.path.join(output_folder, f"cleaned_{output_file}"))
    encoded_df = apply_one_hot_encoding(cleaned_df)
    
    encoded_df.insert(0, 'Order', range(1, len(encoded_df) + 1))
    
    encoded_csv_file = os.path.join(output_folder, f"encoded_{output_file}")
    encoded_df.to_csv(encoded_csv_file, index=False)
    
    print(f"Zapisano zakodowane dane do pliku: {encoded_csv_file}")
    return encoded_df

def collect_shortest_rules(input_folder, output_file):
    order_data = {}
    pattern = os.path.join(input_folder, 'rule_*.csv')

    for file in sorted(glob.glob(pattern)):
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            order = row['Order']
            length = int(row['Rule_Length'])
            rule = row['Rule']
            if order in order_data:
                if length < order_data[order]['min_length']:
                    order_data[order] = {'min_length': length, 'rules': set([rule])}
                elif length == order_data[order]['min_length']:
                    order_data[order]['rules'].add(rule)
            else:
                order_data[order] = {'min_length': length, 'rules': set([rule])}

    max_rules = max(len(data['rules']) for data in order_data.values())
    result = []
    for order, data in order_data.items():
        row = {'Order': order, 'Length': data['min_length']}
        for i, rule in enumerate(data['rules'], 1):
            row[f'Rule_{i}'] = rule
        for i in range(len(data['rules']) + 1, max_rules + 1):
            row[f'Rule_{i}'] = ''
        result.append(row)

    result.sort(key=lambda x: x['Order'])
    fieldnames = ['Order', 'Length'] + [f'Rule_{i}' for i in range(1, max_rules + 1)]

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    print(f"Zapisano zbiorczy plik z najkrótszymi regułami: {output_file}")

def classify_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

# Główna funkcja do przetwarzania subtabel Lymphography
def process_lymphography_tables():
    for i in range(1, 6):
        input_csv = f"../RESULTS/subtable_{i}/1lymphography_reduct_subtable_{i}.csv"
        output_folder = f"../RESULTS/subtable_{i}"
        output_file = f"lymphography_{i}.csv"
        
        # Przetwarzanie i kodowanie danych
        encoded_df = process_and_encode_csv_files(input_csv, output_folder, output_file)
        
        # Klasyfikacja przed optymalizacją
        labels = encoded_df['Class']  # Etykiety klasy
        features = encoded_df.drop(['Order', 'Class'], axis=1)  # Funkcje (cechy)
        accuracy_before = classify_and_evaluate(features, labels)
        print(f"Dokładność przed optymalizacją dla subtabeli {i}: {accuracy_before:.2f}")

        # Zbieranie najkrótszych reguł po optymalizacji
        collect_shortest_rules(output_folder, os.path.join(output_folder, f'shortest_rules_after_optimization_{i}.csv'))

        # Klasyfikacja po optymalizacji (przykładowo, użyj tej samej klasyfikacji)
        accuracy_after = classify_and_evaluate(features, labels)
        print(f"Dokładność po optymalizacji dla subtabeli {i}: {accuracy_after:.2f}")

# Uruchomienie przetwarzania
process_lymphography_tables()
