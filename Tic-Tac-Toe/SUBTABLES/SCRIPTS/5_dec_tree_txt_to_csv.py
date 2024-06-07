import csv
import re

def parse_line(line, attributes):
    parts = line.strip().split(", class: ")
    class_label = parts[1]
    conditions = parts[0].split(") & (")
    conditions[0] = conditions[0][1:]
    conditions[-1] = conditions[-1][:-1]
    
    condition_dict = {attr: "" for attr in attributes}
    condition_dict["Class"] = class_label
    for condition in conditions:
        for key in condition_dict.keys():
            if key in condition:
                condition_dict[key] = condition.strip()
                break
    
    return condition_dict
for i in range(1,6):
    input_file = f"../RESULTS/subtable_{i}/4decision_rules_{i}.txt"
    output_file = f"../RESULTS/subtable_{i}/5decision_rules{i}.csv"

    with open(input_file, "r") as file:
        lines = file.readlines()

    attribute_set = set()
    for line in lines:
        parts = line.strip().split(", class: ")[0]
        conditions = parts.split(") & (")
        conditions[0] = conditions[0][1:] 
        conditions[-1] = conditions[-1][:-1]
        
        for condition in conditions:
            attr_name = condition.split(" ")[0]
            attribute_set.add(attr_name)

    attributes = list(attribute_set)
    attributes.sort()
    attributes.append("Class")

    parsed_lines = [parse_line(line, attributes) for line in lines]
 
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attributes)
        
        writer.writeheader()
        for parsed_line in parsed_lines:
            writer.writerow(parsed_line)

    print(f"Plik CSV został wygenerowany: {output_file}")
