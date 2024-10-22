import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Loop through each subtable file from 1 to 5
for i in range(1, 6):
    classified_data_path = f'../RESULTS/subtable_{i}/classified_test_set_{i}.csv'
    
    # Load the classified data
    try:
        df = pd.read_csv(classified_data_path)

        # Check if the expected columns exist in the DataFrame
        if 'Class' not in df.columns or 'Predicted_Class' not in df.columns:
            raise ValueError(f"Columns 'Class' or 'Predicted_Class' not found in the data for file: {classified_data_path}. Please check the file format.")

        # Wykluczenie przypadków 'Unclassified' i 'nan'
        df = df[(df['Class'] != 'Unclassified') & (df['Predicted_Class'] != 'Unclassified')]
        df = df.dropna(subset=['Class', 'Predicted_Class'])

        # Ensure that the values are of string type
        df['Class'] = df['Class'].astype(str)
        df['Predicted_Class'] = df['Predicted_Class'].astype(str)

        # Automatically detect unique classes, excluding 'Unclassified' and 'nan'
        unique_classes = sorted([cls for cls in df['Class'].unique() if cls not in ['Unclassified', 'nan']])

        # Step 1: Calculate accuracy for filtered data
        accuracy = accuracy_score(df['Class'], df['Predicted_Class'])
        print(f"Results for file: classified_test_set_{i}.csv")
        print(f"Classification Accuracy: {accuracy * 100:.2f}%")

        # Step 2: Generate confusion matrix
        conf_matrix = confusion_matrix(df['Class'], df['Predicted_Class'], labels=unique_classes)
        print("Confusion Matrix:")
        print(conf_matrix)

        # Step 3: Detailed classification report with zero_division=1
        report = classification_report(df['Class'], df['Predicted_Class'], labels=unique_classes, zero_division=1)
        print("Classification Report:")
        print(report)
        print("=" * 50)  # Separator for readability between files

    except FileNotFoundError:
        print(f"File not found: {classified_data_path}. Please make sure the file path is correct.")
    except Exception as e:
        print(f"An error occurred while processing file {classified_data_path}: {e}")
