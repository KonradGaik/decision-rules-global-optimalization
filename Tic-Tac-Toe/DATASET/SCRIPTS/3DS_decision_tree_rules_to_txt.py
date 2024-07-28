import os
import numpy as np
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
            threshold = int(tree_.threshold[node])
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {threshold})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {threshold})"]
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
        feature, operator, value = condition.split(' ', 2)
        feature = feature.strip()
        value = int(value)

        if operator == '<=':
            mask &= df[feature] <= value
        else:
            mask &= df[feature] > value

    matched_rows = df[mask]
    return matched_rows

def process_csv_file(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    
    if df.empty or len(df) <= 1:
        print(f"Plik {csv_file} jest pusty lub zawiera tylko nagłówki.")
        return [], None, None

    df.insert(0, 'Order', range(1, len(df) + 1))
    X = df.drop(columns=['Order', 'class'])
    y = df['class']
    clf = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=1234)
    clf.fit(X, y)

    terminal_rules = get_terminal_rules(clf, X.columns, list(map(str, df['class'].unique())))

    output_file_rules_txt = os.path.join(output_folder, "terminal_rules.txt")
    output_file_rules_csv = os.path.join(output_folder, "terminal_rules.csv")

    with open(output_file_rules_txt, 'w') as f_txt, open(output_file_rules_csv, 'w', newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["Rule", "Class", "Length"])

        for rule_index, rule in enumerate(terminal_rules):
            conditions, decision = rule.split(', class: ')
            rule_length = len(conditions.split(' & '))
            rule_with_length = f"{rule}, length: {rule_length}"
            
            f_txt.write(rule_with_length + '\n')
            csv_writer.writerow([conditions, decision.strip(), rule_length])
            
            matched_rows = match_rules_to_rows(df, rule)
            
            matched_rows['Rule_Length'] = rule_length
            matched_rows['Rule'] = conditions
            
            matched_rows_file = os.path.join(output_folder, f"rule_{rule_index+1}.csv")
            matched_rows.to_csv(matched_rows_file, index=False)

    plt.figure(figsize=(20, 10))
    plot_tree(clf, feature_names=X.columns, class_names=list(map(str, df['class'].unique())), filled=True, rounded=True)
    tree_image_path = os.path.join(output_folder, "decision_tree.jpg")
    plt.savefig(tree_image_path)
    plt.close()
    print(f"Tree image saved to: {tree_image_path}")

    return terminal_rules, X, y

# Specify the input file and output folder
input_csv_file = '../RESULTS/2consistent_tic-tac-toe.csv'
output_folder = '../RESULTS/rules_output/'
os.makedirs(output_folder, exist_ok=True)

if os.path.exists(input_csv_file):
    print(f"Processing file: {input_csv_file}")
    terminal_rules, X, y = process_csv_file(input_csv_file, output_folder)
else:
    print(f"File not found: {input_csv_file}")
