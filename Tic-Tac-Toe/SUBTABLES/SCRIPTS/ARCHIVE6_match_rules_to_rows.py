# import os
# import pandas as pd
# import csv

# def evaluate_rule(data_value, rule_value):
#     if pd.isna(data_value):
#         return False
#     else:
#         return bool(data_value) == bool(rule_value)

# def match_rules_to_rows(data_df, rules_df):
#     matched_rows = []
#     for i, row in data_df.iterrows():
#         row_number = i + 1  
#         matched_rules = []
#         for j, rule_row in rules_df.iterrows():
#             rule = ""
#             rule_length = 0
#             is_matched = True
#             for col_name, rule_value in rule_row.items():
#                 if pd.notna(rule_value):
#                     if col_name not in row.index:
#                         print(f"Column {col_name} not found in data_df at row {i}")
#                         is_matched = False
#                         continue
#                     if pd.isna(row[col_name]):
#                         is_matched = False
#                         continue
#                     if col_name != 'Class':
#                         if evaluate_rule(row[col_name], rule_value):
#                             rule += f"{rule_value} && "
#                             rule_length += 1
#                         else:
#                             is_matched = False
#                             continue
     
#             if is_matched:
#                 matched_rules.append(rule[:-3] + f" => {rule_row['Class']}")
#         if matched_rules:
#             matched_rows.append({'Row Number': row_number, 'Matched Rules': matched_rules})
#     matched_rows_df = pd.DataFrame(matched_rows)
#     return matched_rows_df


# def process_files(base_rules_folder):
#     for i in range(1, 6):
#         csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"3consistent_encoded_modified_tic-tac-toe{i}.csv")
#         csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"5decision_rules{i}.csv")
        
#         data_df = pd.read_csv(csv_file_data)
#         rules_df = pd.read_csv(csv_file_rules)

#         matched_rows = match_rules_to_rows(data_df, rules_df)
        
#         output_file = os.path.join(f"{base_rules_folder}{i}", f"6matched_rows{i}.csv")
#         with open(output_file, mode='w', newline='') as file:
#             csv_writer = csv.writer(file)
#             csv_writer.writerow(['Row Number', 'Matched Rules'])
#             for _, row in matched_rows.iterrows():
#                 csv_writer.writerow([row['Row Number'], row['Matched Rules']])
#         print("Output saved to", output_file)

# if __name__ == "__main__":
#     base_rules_folder = '../RESULTS/subtable_'
#     process_files(base_rules_folder)




# # import pandas as pd
# # import os

# # def evaluate_rule(data_value, rule_value):
# #     if pd.isna(data_value):
# #         return False
# #     else:
# #         return bool(data_value) == bool(rule_value)

# # def match_rules_to_rows(data_df, rules_df):
# #     matched_rows = []
# #     unmatched_rules = []

# #     for i, row in data_df.iterrows():
# #         matched_rules = []

# #         for j, rule_row in rules_df.iterrows():
# #             rule = ""
# #             rule_length = 0  
# #             is_matched = True  

# #             for col_name, rule_value in rule_row.items():
# #                 if pd.notna(rule_value):
# #                     if col_name != 'Class':
# #                         if evaluate_rule(row[col_name], rule_value):
# #                             rule += f"{rule_value} && "
# #                             rule_length += 1
# #                         else:
# #                             is_matched = False
# #                             break
# #                     else:
# #                         if str(row['Class']) != str(rule_value):
# #                             is_matched = False
# #                             break

# #             if is_matched and rule_length > 0:
# #                 matched_rules.append({'Rule': rule[:-4], 'Rule Length': rule_length})
# #             else:
# #                 unmatched_rules.append((i + 1, rule_row))

# #         if matched_rules:
# #             matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})


# #     matched_rows_df = pd.DataFrame(matched_rows)
# #     matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
# #     matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    

    
# #     return matched_rows_df

# # base_rules_folder = '../RESULTS/subtable_'
# # output_folder = '../RESULTS/subtable_'
# # os.makedirs(output_folder, exist_ok=True)

# # for i in range(1, 6):
# #     csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"3consistent_encoded_modified_tic-tac-toe{i}.csv")
# #     csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"5decision_rules{i}.csv")
    
# #     data_df = pd.read_csv(csv_file_data, header=0)
# #     rules_df = pd.read_csv(csv_file_rules, header=0)
    
# #     matched_rows = match_rules_to_rows(data_df, rules_df)
    
# #     output_file = os.path.join(f'{output_folder}{i}', f"6matched_rows{i}.csv")
# #     matched_rows.to_csv(output_file, index=False)

# # print("Dopasowanie reguł zakończone sukcesem.")
