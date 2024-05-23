import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.tree import _tree
import matplotlib.pyplot as plt

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

def process_csv_file(csv_file, output_folder):
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
    print(f"Depth of the tree: {depth}")

    # Get class names and convert to string
    class_names = list(map(str, df['class'].unique()))

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
        for descriptor in descriptors:
            if isinstance(descriptor, str):  # Ensure descriptor is a string before iterating
                for col in X.columns:
                    if col in descriptor:
                        df_rules.at[i, col] = descriptor

    # Save rules to CSV file
    output_file = os.path.join(output_folder, "decision_rules.csv")
    df_rules.to_csv(output_file, index=False)

    # Generate and save the decision tree as a JPG file using matplotlib
    plt.figure(figsize=(20,10))
    plot_tree(clf, feature_names=X.columns, class_names=class_names, filled=True, rounded=True)
    jpg_file = os.path.join(output_folder, "decision_tree.jpg")
    plt.savefig(jpg_file)
    plt.close()

    return rules, X, y

# Path to the single CSV file
csv_file = "../modified_lymphography.csv"

# Output folder for results
output_folder = "DATASET OUTPUT"
os.makedirs(output_folder, exist_ok=True)

# Process the CSV file
rules, X, y = process_csv_file(csv_file, output_folder)
