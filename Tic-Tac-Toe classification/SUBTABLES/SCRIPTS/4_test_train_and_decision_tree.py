import os
import numpy as np
import re
import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.tree import _tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

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

def process_csv_file(csv_file, index, output_folder):
    df = pd.read_csv(csv_file)
    
    # Usuwamy kolumnę 'Order' z danych wejściowych dla drzewa decyzyjnego
    X = df.drop(columns=['Class', 'Order'])
    y = df['Class']

    # Split the data into 70% train and 30% test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234, stratify=y)
    
        # Save train and test sets to CSV files
    train_set = pd.concat([X_train, y_train], axis=1)
    test_set = pd.concat([X_test, y_test], axis=1)

    train_file = os.path.join(f'../RESULTS/subtable_{index}', f'train_set_{index}.csv')
    test_file = os.path.join(f'../RESULTS/subtable_{index}', f'test_set_{index}.csv')

    train_set.to_csv(train_file, index=False)
    test_set.to_csv(test_file, index=False)

    clf = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=1234)
    clf.fit(X_train, y_train)

    # Get terminal rules only from the training set
    terminal_rules = get_terminal_rules(clf, X_train.columns, list(map(str, df['Class'].unique())))

    # Write terminal rules to file (TXT and CSV)
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
            
            # Match rows to this rule and save to CSV
            matched_rows = match_rules_to_rows(X_test, rule)  # Apply rules to the test set
            
            # Add the rule and its length as the last columns
            matched_rows['Rule_Length'] = rule_length
            matched_rows['Rule'] = conditions
            
            # Add back the 'Order' column
            matched_rows = pd.concat([df.loc[matched_rows.index, 'Order'], matched_rows], axis=1)
            
            # Save to CSV in the combined_rules folder
            matched_rows_file = os.path.join(output_folder, f"rule_{index}_{rule_index+1}.csv")
            matched_rows.to_csv(matched_rows_file, index=False)

    # Plot full tree (optional)
    # plt.figure(figsize=(20, 10))
    # plot_tree(clf, feature_names=X_train.columns, class_names=list(map(str, df['Class'].unique())), filled=True, rounded=True)
    # tree_image_path = os.path.join(f"../RESULTS/subtable_{index}", f"3decision_tree_{index}.jpg")
    # plt.savefig(tree_image_path)
    # plt.close()
    # print(f"Tree image saved to: {tree_image_path}")

    return terminal_rules, X_train, X_test, y_train, y_test

output_folder = '../RESULTS/combined_rules/'
os.makedirs(output_folder, exist_ok=True)

base_rules_folder = '../RESULTS/subtable_'
for folder_index in range(1, 6):
    folder_name = f'{base_rules_folder}{folder_index}/'
    csv_file = os.path.join(folder_name, f'3encoded_tic_tac_toe_{folder_index}.csv')
    if os.path.exists(csv_file):
        print(f"Found file: {csv_file}")
        terminal_rules, X_train, X_test, y_train, y_test = process_csv_file(csv_file, folder_index, output_folder)
    else:
        print(f"File not found: {csv_file}")



def process_csv_file(csv_file, index, output_folder):
    # Read the CSV file, ensuring all columns except 'Class' and 'Order' are converted to integer
    df = pd.read_csv(csv_file)
    X = df.drop(columns=['Class'])
    y = df['Class']

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

    # Save train and test sets to CSV files
    train_set = pd.concat([X_train, y_train.reset_index(drop=True)], axis=1)
    test_set = pd.concat([X_test, y_test.reset_index(drop=True)], axis=1)

    train_file = os.path.join(output_folder, f'train_set_{index}.csv')
    test_file = os.path.join(output_folder, f'test_set_{index}.csv')

    train_set.to_csv(train_file, index=False)
    test_set.to_csv(test_file, index=False)
