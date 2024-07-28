import os
import numpy as np
import re
import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.tree import _tree
import matplotlib.pyplot as plt
import hashlib

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

def evaluate_rule(row_value, rule_value):
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    if '>' in rule_value:
        value = float(rule_value.split('>')[-1].strip())
        return row_value > value
    elif '<=' in rule_value:
        value = float(rule_value.split('<=')[-1].strip())
        return row_value <= value
    return False

def match_rules_to_rows(df, rule):
    conditions, decision = rule.split(', class: ')
    conditions = conditions.strip().split(' & ')
    mask = np.ones(len(df), dtype=bool)
    if isinstance(conditions, list):
        conditions = ' & '.join(conditions)

    # Extract each condition from the rule
    condition_list = conditions.split(' & ')
    for condition in condition_list:
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
    X = df.drop(columns=['class'])
    y = df['class']
    clf = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=1234)
    clf.fit(X, y)

    # Get terminal rules only
    terminal_rules = get_terminal_rules(clf, X.columns, list(map(str, df['class'].unique())))

    # Write terminal rules to file (TXT and CSV)
    output_file_rules_txt = os.path.join(f"../RESULTS/subtable_{index}", f"3terminal_rules_{index}.txt")
    output_file_rules_csv = os.path.join(f"../RESULTS/subtable_{index}", f"3terminal_rules_{index}.csv")

    with open(output_file_rules_txt, 'w') as f_txt, open(output_file_rules_csv, 'w', newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["Rule", "Class", "Length"])

        for rule_index, rule in enumerate(terminal_rules):
            conditions, decision = rule.split(', class: ')
            rule_length = len(conditions.split(' & '))
            rule_with_length = f"{rule}, length: {rule_length}"
            
            f_txt.write(rule_with_length + '\n')
            csv_writer.writerow([conditions, decision.strip(), rule_length])
            
            # Create a folder for each terminal rule
            #rule_folder = os.path.join(output_folder, f"rule_{index}_{rule_index+1}_{rule_length}_{decision.strip()}")
            rule_folder = os.path.join(output_folder, f"")
            os.makedirs(rule_folder, exist_ok=True)
            
            # Match rows to this rule and save to CSV
            matched_rows = match_rules_to_rows(df, rule)
            matched_rows_file = os.path.join(rule_folder, f"rule_{index}_{rule_index+1}.csv")
            with open(matched_rows_file, 'w', newline='') as f_matched_csv:
                matched_csv_writer = csv.writer(f_matched_csv)
                matched_csv_writer.writerow([f"Rule: {conditions}, Class: {decision.strip()}, Length: {rule_length}"])
                matched_csv_writer.writerow(matched_rows.columns)
                matched_csv_writer.writerows(matched_rows.values)
    # Plot full tree (optional)
    plt.figure(figsize=(20, 10))
    plot_tree(clf, feature_names=X.columns, class_names=list(map(str, df['class'].unique())), filled=True, rounded=True)
    tree_image_path = os.path.join(f"../RESULTS/subtable_{index}", f"3decision_tree_{index}.jpg")
    plt.savefig(tree_image_path)
    plt.close()
    print(f"Tree image saved to: {tree_image_path}")

    return terminal_rules, X, y

output_folder = '../RESULTS/combined_rules/'
os.makedirs(output_folder, exist_ok=True)

base_rules_folder = '../RESULTS/subtable_'
for folder_index in range(1, 6):
    folder_name = f'{base_rules_folder}{folder_index}/'
    csv_file = os.path.join(folder_name, f'2consistent_modified_lymphography{folder_index}.csv')
    if os.path.exists(csv_file):
        print(f"Found file: {csv_file}")
        terminal_rules, X, y = process_csv_file(csv_file, folder_index, output_folder)
    else:
        print(f"File not found: {csv_file}")
