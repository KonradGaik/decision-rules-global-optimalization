import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# 1. Funkcja do dodawania kolumny z zamówieniem (Order)
def add_order_column(df):
    df.insert(0, 'Order', range(1, len(df) + 1))
    return df

# 2. Funkcja do usuwania niezgodności
def replace_inconsistencies(df):
    # Logika do usuwania niezgodności
    return df.groupby(list(df.columns[:-1]), as_index=False).agg(lambda x: x.value_counts().idxmax())

# 3. Funkcja do indukcji drzewa decyzyjnego
def induce_decision_tree(df):
    X = df.drop(columns=['class'])
    y = df['class']
    clf = DecisionTreeClassifier(criterion='gini', random_state=1234)
    clf.fit(X, y)
    return clf

# 4. Funkcja do przetwarzania podtablic
def process_subtable(df, index):
    # Dodaj Order
    df = add_order_column(df)
    
    # Zastosuj usuwanie niezgodności
    df = replace_inconsistencies(df)
    
    # Podziel na zbiór treningowy i testowy
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=1234)
    
    # Indukcja drzewa decyzyjnego
    clf = induce_decision_tree(train_df)
    
    # Klasyfikacja zbioru testowego
    X_test = test_df.drop(columns=['class'])
    y_test = test_df['class']
    predictions = clf.predict(X_test)
    
    return predictions, y_test

# 5. Funkcja do zbierania wyników i obliczania średniej
def evaluate_results(predictions, y_test):
    accuracy = np.mean(predictions == y_test)
    return accuracy

# 6. Główna logika
def main():
    # Przygotowanie folderu wyników
    output_folder = '../RESULTS'
    os.makedirs(output_folder, exist_ok=True)

    # Wczytaj dane
    df = pd.read_csv('../modified_lymphography.csv')
    # Usuń wiersze, gdzie wszystkie wartości to 'c'
    df = df[~df.apply(lambda row: all(value == 'c' for value in row), axis=1)]
    
    # Zdefiniuj redukty
    reducts = [
        {'block_of_affere', 'changes_in_node', 'changes_in_stru', 'special_forms', 'dislocation_of', 'no_of_nodes_in'},
        {'block_of_affere', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'},
        # ... inne redukty
    ]
    
    accuracies = []

    # Procesuj każdą podtablicę
    for index, reduct in enumerate(reducts, start=1):
        df_selected = df[list(reduct) + ['class']]
        
        # Przetwarzanie podtablicy
        predictions, y_test = process_subtable(df_selected, index)
        
        # Obliczanie dokładności
        accuracy = evaluate_results(predictions, y_test)
        accuracies.append(accuracy)
        
        print(f"Subtable {index}: Accuracy = {accuracy:.2f}")

    # Średnia dokładność z wszystkich podtablic
    average_accuracy = np.mean(accuracies)
    print(f"Average Accuracy: {average_accuracy:.2f}")

if __name__ == "__main__":
    main()
