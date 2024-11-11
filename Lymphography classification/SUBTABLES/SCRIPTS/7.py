# calculate_average.py
import pandas as pd

def calculate_average_accuracy(output_folder, num_subtables, file_suffix):
    accuracies = []
    for i in range(1, num_subtables + 1):
        test_file = f"{output_folder}/subtable_{i}/classified_test_{file_suffix}.csv"
        df = pd.read_csv(test_file)
        accuracy = (df['class'] == df[f'predicted_class_{file_suffix}']).mean()
        accuracies.append(accuracy)
    average_accuracy = sum(accuracies) / len(accuracies)
    print(f"Średnia dokładność dla klasyfikacji {file_suffix}: {average_accuracy * 100:.2f}%")

# Użycie
output_folder = "../RESULTS"
num_subtables = 5
calculate_average_accuracy(output_folder, num_subtables, "before")  # Średnia dla klasyfikacji przed optymalizacją
calculate_average_accuracy(output_folder, num_subtables, "after")   # Średnia dla klasyfikacji po optymalizacji
