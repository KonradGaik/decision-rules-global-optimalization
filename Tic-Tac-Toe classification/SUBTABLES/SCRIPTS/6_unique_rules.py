import pandas as pd

def extract_unique_rules_from_summary(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Create an empty DataFrame to store unique rules and their classes
    unique_rules_list = []

    # Loop through each row in the DataFrame
    for _, row in df.iterrows():
        rule_class = row['Class']  # Get the class for the current row

        # Iterate over the Rule columns and add each non-empty rule to the unique_rules_list
        for i in range(1, 6):  # Assuming there are at most 5 rules (Rule_1 to Rule_5)
            rule = row.get(f'Rule_{i}')
            if pd.notna(rule):  # Check if the rule is not NaN
                unique_rules_list.append({'Rule': rule, 'Class': rule_class})

    # Convert the list of unique rules to a DataFrame
    unique_rules_df = pd.DataFrame(unique_rules_list)

    # Drop duplicate rules to ensure uniqueness
    unique_rules_df = unique_rules_df.drop_duplicates().sort_values(by=['Rule', 'Class'])

    # Save the unique rules to the output CSV file
    unique_rules_df.to_csv(output_file, index=False)

# Set the input file and output file paths
input_file = '../RESULTS/shortest_rules_summary.csv'
output_file = '../RESULTS/unique_decision_rules_shortest.csv'

# Run the function to extract unique decision rules
extract_unique_rules_from_summary(input_file, output_file)

print(f"Unique decision rules saved to {output_file}")
