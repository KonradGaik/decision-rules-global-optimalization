import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree

# Funkcja do uzyskiwania reguł decyzyjnych z drzewa
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
            path += [(class_names[int(np.argmax(tree_.value[node]))], tree_.n_node_samples[node])]
            paths += [path]
            
    recurse(0, path, paths)

    # Sortowanie ścieżek według liczby próbek
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]
    
    rules = []
    for path in paths:
        rule = "if "
        
        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if len(path) == 1:  # Jeśli tylko jednen warunek
             rule += f"Class:{path[-1][0]}"
        else:
            response = path[-1][0]
            rule += f"Class:{response}"
        rules += [rule]
        
    return rules

# Funkcja do przetwarzania każdego pliku
def process_csv_file(csv_file, index):
    # Odczyt danych z pliku CSV
    df = pd.read_csv(csv_file)
    
    # Oddzielenie cech od zmiennej docelowej
    X = df.drop(columns=['class'])
    y = df['class']

    # Uczenie klasyfikatora drzewa decyzyjnego
    clf = DecisionTreeClassifier(criterion='gini', random_state=1234)
    clf.fit(X, y)

    # Pobranie nazw klas
    class_names = df['class'].unique()

    # Pobranie reguł
    rules = get_rules(clf, X.columns, class_names)

    return rules, index

# Nazwa folderu zawierającego pliki CSV
folder_name = "2consistent_data"

# Nowy folder do zapisywania wyników
output_folder = "3decision_rules"
os.makedirs(output_folder, exist_ok=True)

# Iteracja po wszystkich plikach w folderze
for i, file_name in enumerate(sorted(os.listdir(folder_name)), start=1):
    if file_name.endswith(".csv"):
        # Utworzenie ścieżki do pliku CSV
        csv_file = os.path.join(folder_name, file_name)
        
        # Przetwarzanie pliku CSV
        rules, file_index = process_csv_file(csv_file, i)
        
        # Zapisywanie reguł do pliku
        output_file = os.path.join(output_folder, f"decision_rules_{file_index}_sort.txt")
        with open(output_file, "w") as f:
            for rule in rules:
                f.write(rule + "\n")
