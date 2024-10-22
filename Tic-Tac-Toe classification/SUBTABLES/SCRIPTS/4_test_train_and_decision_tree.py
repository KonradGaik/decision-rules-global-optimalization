import os
import numpy as np
import re
import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from sklearn.model_selection import train_test_split
import glob
from sklearn.model_selection import cross_val_score

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
            # If the node is not a leaf, continue recursion
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            # If it is a leaf, append the path to the class
            class_index = np.argmax(tree_.value[node])
            class_decision = class_names[class_index]
            rule = f"{' & '.join(path)}, class: {class_decision}"
            paths.append(rule)

    recurse(0, path, paths)
    return paths

def match_rules_to_rows(df, rule):
    try:
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

    except Exception as e:
        print(f"Error matching rule: {rule}, Error: {e}")
        return pd.DataFrame()  # Empty DataFrame if error occurs

def process_csv_file(csv_file, index, output_folder):
    df = pd.read_csv(csv_file)
    
    # Ensure 'Class' and 'Order' are in the DataFrame
    if 'Class' not in df.columns or 'Order' not in df.columns:
        raise ValueError(f"'Class' or 'Order' column missing in {csv_file}")

    # Drop 'Class' and 'Order' for feature selection
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

    clf = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=1234)
    scores = cross_val_score(clf, X_train, y_train, cv=5)

    print("Cross-validation accuracy: ", scores.mean())
    clf.fit(X_train, y_train)

    # Get terminal rules only from the training set
    terminal_rules = get_terminal_rules(clf, X_train.columns, list(map(str, df['Class'].unique())))

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
            
            # Match rows to this rule and save to CSV
            matched_rows = match_rules_to_rows(X_test, rule)  # Apply rules to the test set
            
            if not matched_rows.empty:
                matched_rows = matched_rows.copy()  # Avoid SettingWithCopyWarning
                matched_rows.loc[:, 'Rule_Length'] = rule_length
                matched_rows.loc[:, 'Rule'] = conditions
                matched_rows.loc[:, 'Class'] = decision
                
                # Add back the 'Order' column
                matched_rows = pd.concat([df.loc[matched_rows.index, 'Order'], matched_rows], axis=1)
                
                # Save to CSV in the combined_rules folder
                matched_rows_file = os.path.join(output_folder, f"rule_{index}_{rule_index+1}.csv")
                matched_rows.to_csv(matched_rows_file, index=False)
            else:
                print(f"No matching rows for rule: {rule}")

    # Add a summary of lengths and rules to a CSV file specific to each subtable
    summary_file = os.path.join(f'../RESULTS/subtable_{index}', f'combined_order_lengths_and_rules_summary_{index}.csv')
    with open(summary_file, 'w', newline='') as f_summary:
        csv_summary_writer = csv.writer(f_summary)
        csv_summary_writer.writerow(['Rule_Index', 'Conditions', 'Class', 'Length'])

        for rule_index, rule in enumerate(terminal_rules):
            conditions, decision = rule.split(', class: ')
            rule_length = len(conditions.split(' & '))
            csv_summary_writer.writerow([rule_index + 1, conditions, decision.strip(), rule_length])

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

def collect_order_lengths_and_rules(input_folder, output_file):
    # Dictionary to store data
    order_data = {}

    # Pattern for rule files
    pattern = os.path.join(input_folder, 'rule_*.csv')

    # Iterate over all matching files
    for file in sorted(glob.glob(pattern)):
        # Read the CSV file
        df = pd.read_csv(file)

        # Check if 'Order' and 'Rule_Length' columns exist
        if 'Order' not in df.columns or 'Rule_Length' not in df.columns:
            raise ValueError(f"'Order' or 'Rule_Length' column missing in {file}")

        # Iterate over DataFrame rows
        for _, row in df.iterrows():
            order = row['Order']
            length = int(row['Rule_Length'])  # Convert to int
            rule = row['Rule']
            class_label = row['Class'] if 'Class' in row else None  # Safe assignment of class

            # If Order already exists in the dictionary, add length and rule to lists
            if order in order_data:
                order_data[order]['lengths'].append(length)
                order_data[order]['rules'].append(rule)

                # Only add the class if it hasn't been added before
                if order_data[order]['class'] is None and class_label is not None:
                    order_data[order]['class'] = class_label
            else:
                # If not, create new lists with this length, rule, and class
                order_data[order] = {
                    'lengths': [length],
                    'rules': [rule],
                    'class': class_label  # Initialize class
                }

    # Creating results list
    result = []
    max_length = max(len(data['lengths']) for data in order_data.values())
    
    for order, data in order_data.items():
        row = {'Order': order}
        for i in range(max_length):
            if i < len(data['lengths']):
                row[f'Length_{i+1}'] = data['lengths'][i]
                row[f'Rule_{i+1}'] = data['rules'][i]
            else:
                row[f'Length_{i+1}'] = ''
                row[f'Rule_{i+1}'] = ''
        
        # Include only one class for the order
        row['Class'] = data['class'] if data['class'] is not None else ''
        result.append(row)

    # Sorting results by Order
    result.sort(key=lambda x: x['Order'])

    # Saving to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Order'] + [f'Length_{i+1}' for i in range(max_length)] + \
                     [f'Rule_{i+1}' for i in range(max_length)] + ['Class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in result:
            writer.writerow(row)

# Call the function with the combined rules folder
output_summary_file = os.path.join('../RESULTS', 'combined_order_lengths_and_rules_summary.csv')
collect_order_lengths_and_rules(output_folder, output_summary_file)
