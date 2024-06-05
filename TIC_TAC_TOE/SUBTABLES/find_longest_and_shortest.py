import os
import pandas as pd

def get_rule_length(rule):
    return rule.count(' && ') + 1 if ' && ' in rule else 1

def find_shortest_and_longest_rules(matched_rows_df):
    matched_rows_df['Rule Length'] = matched_rows_df['Matched Rules'].apply(lambda x: get_rule_length(x[0]) if x else 0)
    
    shortest_rule_row = matched_rows_df.loc[matched_rows_df['Rule Length'].idxmin()]
    longest_rule_row = matched_rows_df.loc[matched_rows_df['Rule Length'].idxmax()]
    
    shortest_rule = shortest_rule_row['Matched Rules'][0]
    longest_rule = longest_rule_row['Matched Rules'][0]
    
    return shortest_rule, longest_rule, shortest_rule_row['Rule Length'], longest_rule_row['Rule Length']

base_rules_folder = 'subtable_'

for i in range(1, 6):
    matched_rows_file = os.path.join(f"{base_rules_folder}{i}", f"matched_rows_shortest_{i}.csv")
    
    matched_rows_df = pd.read_csv(matched_rows_file)
    matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: eval(x))
    
    shortest_rule, longest_rule, shortest_length, longest_length = find_shortest_and_longest_rules(matched_rows_df)
    
    print(f"Subtable {i}:")
    print(f"Shortest Rule (Length {shortest_length}): {shortest_rule}")
    print(f"Longest Rule (Length {longest_length}): {longest_rule}")
    print()
