# classify_test_set.py
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def classify_test_set(train_file, test_file, output_file):
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    X_train = train_df.drop(columns=['class'])
    y_train = train_df['class']
    X_test = test_df.drop(columns=['class'])
    y_test = test_df['class']
    
    clf = DecisionTreeClassifier(criterion="gini", max_depth=None, random_state=42)
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    accuracy = (predictions == y_test).mean()
    test_df['predicted_class'] = predictions
    test_df.to_csv(output_file, index=False)
    print(f"Klasyfikacja zakończona. Skuteczność: {accuracy * 100:.2f}%")

# Użycie
for i in range(1, 6):
    train_file = f"../RESULTS/subtable_{i}/train.csv"
    test_file = f"../RESULTS/subtable_{i}/test.csv"
    output_file = f"../RESULTS/subtable_{i}/classified_test.csv"
    classify_test_set(train_file, test_file, output_file)
