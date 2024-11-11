# decision_tree_induction.py
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

def induce_decision_tree(train_file, output_file):
    df = pd.read_csv(train_file)
    X = df.drop(columns=['Class'])
    y = df['Class']
    clf = DecisionTreeClassifier(criterion="gini", max_depth=None, random_state=1234)
    clf.fit(X, y)
    rules = export_text(clf, feature_names=list(X.columns))
    with open(output_file, 'w') as f:
        f.write(rules)
    print("Reguły drzewa decyzyjnego zapisane:", output_file)

# Użycie
for i in range(1, 6):
    train_file = f"../RESULTS/subtable_{i}/train.csv"
    output_file = f"../RESULTS/subtable_{i}/rules.txt"
    induce_decision_tree(train_file, output_file)
