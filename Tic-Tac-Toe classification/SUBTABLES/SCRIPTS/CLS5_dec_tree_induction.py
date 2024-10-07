import os
import numpy as np
import re
import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.tree import _tree
import matplotlib.pyplot as plt

def get_terminal_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    paths = []
    path = []

    def recurse(node, path, paths):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            class_index = np.argmax(tree_.value[node])
            class_decision = class_names[class_index]
            rule = f"{' & '.join(path)}, class: {class_decision}"
            paths.append(rule)
    recurse(0, path, paths)
    return paths

def match_rules_to_rows(df, rule):
    conditions, decision = rule.split(', class: ')
    conditions = conditions.strip().split(' & ')
    mask = np.ones(len(df), dtype=bool)

    for condition in conditions:
        condition = condition.strip('()')
        feature, operator, value = re.split(r'([<>=]+)', condition)
        feature = feature.strip()
        value = float(value.strip())

        if operator == '<=':
            mask &= df[feature] <= value
        elif operator == '>':
            mask &= df[feature] > value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    matched_rows = df[mask]
    return matched_rows

def process_training_data(index, output_folder):
    # Wczytaj dane treningowe
    train_file = f'../RESULTS/subtable_{index}/train_data.csv'
    df = pd.read_csv(train_file)

    # Oddziel cechy i etykiety
    X = df.drop(columns=['Class'])
    y = df['Class']

    # Tworzenie i dopasowanie modelu drzewa decyzyjnego
    clf = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=1234)
    clf.fit(X, y)

    # Ekstrakcja terminalnych reguł
    terminal_rules = get_terminal_rules(clf, X.columns, list(map(str, df['Class'].unique())))

    # Zapis reguł do plików (TXT i CSV)
    output_file_rules_txt = os.path.join(f"../RESULTS/subtable_{index}", f"3terminal_rules_{index}.txt")
    output_file_rules_csv = os.path.join(f"../RESULTS/subtable_{index}", f"3terminal_rules_{index}.csv")

    with open(output_file_rules_txt, 'w') as f_txt, open(output_file_rules_csv, 'w', newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["Rule", "class", "Length"])

        for rule_index, rule in enumerate(terminal_rules):
            conditions, decision = rule.split(', class: ')
            rule_length = len(conditions.split(' & '))
            rule_with_length = f"{rule}, length: {rule_length}"

            f_txt.write(rule_with_length + '\n')
            csv_writer.writerow([conditions, decision.strip(), rule_length])

            # Dopasuj wiersze do tej reguły i zapisz do CSV
            matched_rows = match_rules_to_rows(X, rule).copy()  # Dodaj .copy()

            # Dodaj długość reguły i regułę jako ostatnie kolumny
            matched_rows.loc[:, 'Rule_Length'] = rule_length
            matched_rows.loc[:, 'Rule'] = conditions

            # Zapisz do CSV w folderze wynikowym
            if not matched_rows.empty:
                matched_rows_file = os.path.join(output_folder, f"rule_{index}_{rule_index + 1}.csv")
                matched_rows.to_csv(matched_rows_file, index=False)
            else:
                print(f"No matching rows for rule {rule}.")
    return terminal_rules

# Folder do zapisu wyników
output_folder = '../RESULTS/combined_rules/'
os.makedirs(output_folder, exist_ok=True)

# Procesuj dane treningowe dla każdej podtablicy
for folder_index in range(1, 6):
    print(f"Processing subtable {folder_index}...")
    process_training_data(folder_index, output_folder)