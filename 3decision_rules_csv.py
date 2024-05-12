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

# Funkcja do przetwarzania każdego pliku CSV
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

    # Konwersja reguł do ramki danych
    df_rules = pd.DataFrame(columns=["Decision"] + [f"Descriptor_{i}" for i in range(1, len(X.columns) + 1)])
    for i, rule in enumerate(rules, start=1):
        descriptors = rule.split(" & ")
        decision = descriptors[-1].split(" => ")[1]
        descriptors = descriptors[:-1]
        descriptors.extend([np.nan] * (len(X.columns) - len(descriptors)))  # Uzupełnienie brakujących deskryptorów
        df_rules.at[i, "Decision"] = decision
        for j, descriptor in enumerate(descriptors, start=1):
            df_rules.at[i, f"Descriptor_{j}"] = descriptor

    return df_rules

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
        df_rules = process_csv_file(csv_file, i)
        
        # Zapisywanie reguł do pliku CSV
        output_file = os.path.join(output_folder, f"decision_rules_{i}.csv")
        df_rules.to_csv(output_file, index=False)
