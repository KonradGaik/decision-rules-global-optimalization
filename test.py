import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text

# Wczytaj dane
data = pd.read_csv("modified_lymphography_reduct_subtable_4.csv")

# Podziel dane na atrybuty i etykiety
X = data.drop(columns=['class'])
y = data['class']

# Utwórz i wytrenuj klasyfikator drzewa decyzyjnego
clf = DecisionTreeClassifier(criterion='gini', max_depth=3)
clf.fit(X, y)

# Pobierz reguły decyzyjne
rules = export_text(clf, feature_names=X.columns.tolist())
print("Reguły decyzyjne:")
print(rules)
