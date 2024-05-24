import os
import pandas as pd

for x in range(5):
    print(x)
    if not os.path.exists(f'subtable_{x+1}'):
        os.makedirs(f'subtable_{x+1}')

# KROK 1 
# Utworzenie podtablic z reduktów
# Wczytaj plik CSV
df = pd.read_csv('modified_lymphography.csv')

# Usuwanie wierszy zawierających ciąg 'c,c,c,c,c,c' w dowolnej kolejności
df = df[~df.apply(lambda row: all(value == 'c' for value in row), axis=1)]

# Lista reductów
reducts = [
    {'block_of_affere', 'changes_in_node', 'changes_in_stru', 'special_forms', 'dislocation_of', 'no_of_nodes_in'},
    {'block_of_affere', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'},
    {'block_of_affere', 'changes_in_lym', 'defect_in_node', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_lym', 'changes_in_node', 'changes_in_stru', 'special_forms', 'no_of_nodes_in'},
    {'block_of_affere', 'early_uptake_in', 'changes_in_node', 'changes_in_stru', 'special_forms', 'exclusion_of_no', 'no_of_nodes_in'}
]

# Iteruj przez każdy reduct
for idx, reduct in enumerate(reducts, start=1):
    # Wybierz tylko wybrane kolumny, dodaj 'class' na końcu
    df_selected = df[list(reduct) + ['class']]
    # Zapisz wybrane kolumny do nowego pliku CSV w folderze "subtables"
    df_selected.to_csv(os.path.join(f'subtable_{idx}', f'1lymphography_reduct_subtable_{idx}.csv'), index=False)
