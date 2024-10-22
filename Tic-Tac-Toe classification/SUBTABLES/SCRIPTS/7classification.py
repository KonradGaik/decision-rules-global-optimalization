import os
import pandas as pd

# Step 1: Load decision rules from a CSV file
rules_file_path = '../RESULTS/unique_decision_rules_shortest.csv'
rules_df = pd.read_csv(rules_file_path)

# Convert rules DataFrame into a list of dictionaries with correct key names
rules = rules_df.rename(columns={'Rule': 'conditions', 'Class': 'class'}).to_dict(orient='records')

# Step 2: Define a function to evaluate rule conditions for each row
def evaluate_rule_conditions(row, rule_conditions):
    # Podziel warunki reguł na pojedyncze warunki
    conditions = rule_conditions.split(' & ')
    
    # Sprawdzaj każdy warunek z osobna
    for condition in conditions:
        try:
            feature, operator, value = condition.strip('()').split(' ')
            value = float(value)

            # Sprawdź, czy kolumna istnieje w danych
            if feature not in row.index:
                print(f"Warning: Column '{feature}' not found in the data. Skipping this rule for this subtable.")
                return False  # Pomijamy tę regułę dla tego wiersza
            
            if operator == '<=':
                if not row[feature] <= value:
                    return False
            elif operator == '>':
                if not row[feature] > value:
                    return False
            else:
                print(f"Unsupported operator: {operator}")
                return False
        except ValueError as e:
            print(f"Error parsing condition: {condition} with error: {e}")
            return False
    
    return True

# Step 3: Classify test data using decision rules
def classify_row(row, rules):
    for rule in rules:
        if evaluate_rule_conditions(row, rule['conditions']):
            return rule['class']
    return 'Unclassified'  # If no rules match, return a default value

# Step 4: Loop through each subtable's test dataset and classify
for i in range(1, 6):  # Adjust the range if you have more or fewer subtables
    test_data_path = f'../RESULTS/subtable_{i}/test_set_{i}.csv'
    
    if os.path.exists(test_data_path):
        # Load the test data
        test_data = pd.read_csv(test_data_path)
        
        # Apply classification to the test data
        test_data['Predicted_Class'] = test_data.apply(classify_row, axis=1, rules=rules)

        # test_data['Predicted_Class'] = test_data['Predicted_Class'].replace({'positive': 'negative', 'negative': 'positive'})
        
        # Save the classified test data
        classified_data_path = f'../RESULTS/subtable_{i}/classified_test_set_{i}.csv'
        test_data.to_csv(classified_data_path, index=False)
        
        print(f"Classification complete for subtable {i}. Results saved to {classified_data_path}")
    else:
        print(f"Test data file not found: {test_data_path}")