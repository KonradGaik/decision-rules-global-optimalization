import pandas as pd

def count_unique_rules(file_path, inx):

    df = pd.read_csv(file_path)
    

    def unique_rule_count(matched_rules_str):
        try:
            rules = matched_rules_str.strip('[]').split(', ')
            unique_rules = set(rules)
            return len(unique_rules)
        except Exception as e:
            print(f"Error parsing rules: {e}")
            return 0

    df['Unique Rule Count'] = df['Matched Rules'].apply(unique_rule_count)
    
    output_file_path = (f'../RESULTS/subtable_{inx}/10before_unique_rule_count_{inx}.csv')
    df.to_csv(output_file_path, index=False)
    return output_file_path

for i in range(1, 6):
    file_path = f'../RESULTS/subtable_{i}/6matched_rows{i}.csv'
    output_file = count_unique_rules(file_path, i)
    print(f"Wynik zapisano do: {output_file}")
