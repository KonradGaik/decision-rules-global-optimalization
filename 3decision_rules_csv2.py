import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree

def get_rules(tree, feature_names, class_names):
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
            p1 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            class_index = np.argmax(tree_.value[node])
            class_decision = class_names[class_index]
            rule = " & ".join(path) + f" => {class_decision}"
            paths.append(rule)
            
    recurse(0, path, paths)

    return paths

# Function to process each CSV file
def process_csv_file(csv_file, index):
    # Read data from the CSV file
    df = pd.read_csv(csv_file)
    
    # Separate features from the target variable
    X = df.drop(columns=['class'])
    y = df['class']

    # Train the decision tree classifier
    clf = DecisionTreeClassifier(criterion='gini', random_state=1234)
    clf.fit(X, y)
    # Check the depth of the tree
    depth = clf.tree_.max_depth
    print(f"Głębokość drzewa {index} ", depth)
    # Get class names
    class_names = df['class'].unique()

    # Get rules
    rules = get_rules(clf, X.columns, class_names)

    # Initialize an empty DataFrame to store rules
    df_rules = pd.DataFrame(columns=X.columns)  # Create columns for each attribute
    for i, rule in enumerate(rules, start=1):
        descriptors = rule.split(" & ")
        decision = descriptors[-1].split(" => ")[1]
        descriptors = descriptors[:-1]
        descriptors.extend([np.nan] * (len(X.columns) - len(descriptors)))  # Fill missing descriptors
        df_rules.at[i, "class"] = decision
        for j, descriptor in enumerate(descriptors, start=1):
            if isinstance(descriptor, str):  # Check if descriptor is a string
                for col in X.columns:
                    if col in descriptor:
                        df_rules.at[i, col] = descriptor

    return df_rules


# Folder containing CSV files
folder_name = "2consistent_data"

# Output folder for results
output_folder = "3decision_rules"
os.makedirs(output_folder, exist_ok=True)

# Iterate over all files in the folder
for i, file_name in enumerate(sorted(os.listdir(folder_name)), start=1):
    if file_name.endswith(".csv"):
        # Create path to CSV file
        csv_file = os.path.join(folder_name, file_name)
        
        # Process CSV file
        df_rules_result = process_csv_file(csv_file, i)
        
        # Save rules to CSV file
        output_file = os.path.join(output_folder, f"decision_rules_{i}_2.csv")
        df_rules_result.to_csv(output_file, index=False)