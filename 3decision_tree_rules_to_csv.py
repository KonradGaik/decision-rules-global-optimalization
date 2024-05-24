import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

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

def process_csv_file(csv_file, index, output_folder):
    df = pd.read_csv(csv_file)
    X = df.drop(columns=['class'])
    y = df['class']
    clf = DecisionTreeClassifier(criterion='gini', random_state=1234)
    clf.fit(X, y)
    depth = clf.tree_.max_depth
    print(f"Głębokość drzewa {index}: {depth}")
    class_names = list(map(str, df['class'].unique()))
    rules = get_rules(clf, X.columns, class_names)

    output_file = os.path.join(output_folder, f"3decision_rules_{index}.txt")
    with open(output_file, 'w') as f:
        for rule in rules:
            f.write(rule + '\n')

    # Generowanie i zapisywanie drzewa decyzyjnego jako plik JPG
    plt.figure(figsize=(20,10))
    plot_tree(clf, feature_names=X.columns, class_names=class_names, filled=True, rounded=True)
    tree_image_path = os.path.join(output_folder, f"3decision_tree_{index}.jpg")
    plt.savefig(tree_image_path)
    plt.close()
    print(f"Tree image saved to: {tree_image_path}")

    return rules, X, y

for folder_index in range(1, 6):
    folder_name = f'subtable_{folder_index}'
    csv_file = os.path.join(folder_name, f'1lymphography_reduct_subtable_{folder_index}.csv')
    if os.path.exists(csv_file):
        print(f"Found file: {csv_file}")
        rules, X, y = process_csv_file(csv_file, folder_index, folder_name)
    else:
        print(f"File not found: {csv_file}")
