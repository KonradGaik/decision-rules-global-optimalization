import pandas as pd

# Path to the input and output CSV files
input_file = "../RESULTS/order_lengths_and_rules_summary.csv"
output_file = "../RESULTS/unique_decision_rules.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Initialize a set to store unique rules
unique_rules = set()

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract rules from columns 'Rule_1' to 'Rule_5'
    rules_in_row = [row[col] for col in df.columns if col.startswith('Rule_')]
    
    # Add rules to the set of unique rules
    unique_rules.update(rules_in_row)

# Convert the set of unique rules into a DataFrame
unique_rules_df = pd.DataFrame(list(unique_rules), columns=['Unique_Rules'])

# Write the unique rules DataFrame to a new CSV file
unique_rules_df.to_csv(output_file, index=False)

print(f"Unique decision rules extracted and saved to {output_file}.")

