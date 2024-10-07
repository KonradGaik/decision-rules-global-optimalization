# from typing import List, Tuple
# import pandas as pd
# from sklearn.metrics import accuracy_score
# from sklearn.calibration import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from gen_opt import generate_shortest_rules

# class DecisionRuleOptimizer:
#     def __init__(self, data: pd.DataFrame):
#         self.data = data

#     def create_decision_table(self) -> pd.DataFrame:
#         return self.data

#     def generate_reducts(self) -> List[pd.DataFrame]:
#         return [self.data]

#     def create_subtables(self, reducts: List[pd.DataFrame]) -> List[pd.DataFrame]:
#         return reducts

#     def split_data(self, subtable: pd.DataFrame, random_state: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
#         return train_test_split(subtable, test_size=0.3, random_state=random_state)

#     def induce_tree(self, train_data: pd.DataFrame, max_depth: int = None) -> DecisionTreeClassifier:
#         X_train = train_data.drop('Class', axis=1)
#         y_train = train_data['Class']

#         label_encoder = LabelEncoder()
#         y_train_encoded = label_encoder.fit_transform(y_train)

#         X_train_encoded = X_train.apply(pd.to_numeric, errors='coerce')

#         # Ustal hiperparametry, np. max_depth
#         model = DecisionTreeClassifier(max_depth=max_depth)
#         model.fit(X_train_encoded, y_train_encoded)

#         return model

#     def classify(self, model: DecisionTreeClassifier, test_data: pd.DataFrame) -> pd.Series:
#         X_test = test_data.drop('Class', axis=1)
#         y_test = test_data['Class']

#         label_encoder = LabelEncoder()
#         y_test_encoded = label_encoder.fit_transform(y_test)

#         X_test_encoded = X_test.apply(pd.to_numeric, errors='coerce')

#         predictions_encoded = model.predict(X_test_encoded)
#         predictions = label_encoder.inverse_transform(predictions_encoded)

#         return predictions

#     def optimize_rules(self, model: DecisionTreeClassifier) -> List[str]:
#         generate_shortest_rules()
#         rules_df = pd.read_csv('../RESULTS/shortest_rules_with_length.csv')
#         return rules_df['Rule'].tolist()

#     def run_experiment(self, iterations: int = 5, max_depth: int = None) -> List[float]:
#         average_accuracies = []
#         for i in range(iterations):
#             decision_table = self.create_decision_table()
#             reducts = self.generate_reducts()
#             subtables = self.create_subtables(reducts)

#             for subtable in subtables:
#                 train_data, test_data = self.split_data(subtable, random_state=i)
#                 model = self.induce_tree(train_data, max_depth=max_depth)
#                 rules = self.optimize_rules(model)
#                 predictions = self.classify(model, test_data)

#                 accuracy = accuracy_score(test_data['Class'], predictions)
#                 average_accuracies.append(accuracy)

#         return average_accuracies

# if __name__ == "__main__":
#     for i in range(1, 6):
#         data = pd.read_csv(f'../RESULTS/subtable_{i}/1tic_tac_toe_reduct_subtable_{i}.csv')

#         optimizer = DecisionRuleOptimizer(data)

#         # Możesz eksperymentować z różnymi wartościami max_depth
#         accuracies = optimizer.run_experiment(iterations=5, max_depth=5)
#         accuracies_rounded = [round(acc, 2) for acc in accuracies]
#         print(f"Average accuracies for SUBTABLE '{i}' each iteration {accuracies_rounded}")
#         print("Overall average accuracy:", round(sum(accuracies) / len(accuracies), 2))
