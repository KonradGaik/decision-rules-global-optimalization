# calculate_average.py
import pandas as pd

def calculate_average_accuracy(output_folder, num_subtables):
    accuracies = []
    for i in range(1, num_subtables + 1):
        test_file = f"{output_folder}/subtable_{i}/classified_test.csv"
        df = pd.read_csv(test_file)
        accuracy = (df['class'] == df['predicted_class']).mean()
        accuracies.append(accuracy)
    average_accuracy = sum(accuracies) / len(accuracies)
    print(f"Średnia dokładność z testowych podtablic: {average_accuracy * 100:.2f}%")

# Użycie
output_folder = "../RESULTS"
num_subtables = 5
calculate_average_accuracy(output_folder, num_subtables)
