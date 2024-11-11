import os
import numpy as np
import re
import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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
    if ', class: ' not in rule:
        print(f"Warning: Rule does not contain class information: {rule}")
        return pd.DataFrame()

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

def process_csv_file(csv_file, index, output_folder):
    df = pd.read_csv(csv_file)
    
    # Podział na zbiór treningowy i testowy
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=1234, stratify=df['Class'])

    # Zapisujemy zbiory do plików
    train_file = os.path.join(output_folder, f"train_set_{index}.csv")
    test_file = os.path.join(output_folder, f"test_set_{index}.csv")
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    # Przygotowanie danych do trenowania
    X_train = train_df.drop(columns=['Class', 'Order'])
    y_train = train_df['Class']
    
    # Trenujemy model
    clf = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=1234)
    clf.fit(X_train, y_train)

    # Generowanie reguł terminalnych
    terminal_rules = get_terminal_rules(clf, X_train.columns, list(map(str, df['Class'].unique())))

    # Zapisywanie reguł do plików
    output_file_rules_txt = os.path.join(output_folder, f"3terminal_rules_{index}.txt")
    output_file_rules_csv = os.path.join(output_folder, f"3terminal_rules_{index}.csv")

    with open(output_file_rules_txt, 'w') as f_txt, open(output_file_rules_csv, 'w', newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["Rule", "Class", "Length"])

        for rule_index, rule in enumerate(terminal_rules):
            if ', class: ' not in rule:
                print(f"Warning: Skipping rule without class: {rule}")
                continue
            
            conditions, decision = rule.split(', class: ')
            decision = decision.strip()
            rule_length = len(conditions.split(' & '))
            rule_with_length = f"{conditions}, class: {decision}, length: {rule_length}"
            
            f_txt.write(rule_with_length + '\n')
            csv_writer.writerow([conditions, decision, rule_length])
            
            # Dopasowanie reguł do wierszy zbioru testowego
            matched_rows = match_rules_to_rows(test_df, f"{conditions}, class: {decision}")
            
            if not matched_rows.empty:
                matched_rows['Rule_Length'] = rule_length
                matched_rows['Rule'] = conditions
                matched_rows['Decision_Class'] = decision
                
                matched_rows = pd.concat([test_df.loc[matched_rows.index, 'Order'], matched_rows], axis=1)
                
                matched_rows_file = os.path.join(output_folder, f"rule_{index}_{rule_index+1}.csv")
                matched_rows.to_csv(matched_rows_file, index=False)

    # Klasyfikacja na zbiorze testowym
    X_test = test_df.drop(columns=['Class', 'Order'])
    y_test = test_df['Class']
    y_pred = clf.predict(X_test)
    
    # Zapis wyników klasyfikacji do pliku CSV
    test_df['Predicted_Class'] = y_pred
    classification_results_file = os.path.join(output_folder, f"classification_results_{index}.csv")
    test_df[['Order', 'Class', 'Predicted_Class']].to_csv(classification_results_file, index=False)

    # Obliczanie dokładności
    accuracy = accuracy_score(y_test, test_df['Predicted_Class']) * 100
    with open(classification_results_file, 'a') as f:
        f.write(f'\nDokładność klasyfikacji: {accuracy:.2f}%\n')

    print(f"Przetworzono plik {csv_file} z dokładnością {accuracy:.2f}%.")

output_folder = '../RESULTS/combined_rules/'
os.makedirs(output_folder, exist_ok=True)

base_rules_folder = '../RESULTS/subtable_'
for folder_index in range(1, 6):
    folder_name = f'{base_rules_folder}{folder_index}/'
    csv_file = os.path.join(folder_name, f'3encoded_tic_tac_toe_{folder_index}.csv')
    if os.path.exists(csv_file):
        print(f"Found file: {csv_file}")
        process_csv_file(csv_file, folder_index, output_folder)
    else:
        print(f"File not found: {csv_file}")
