import os
import pandas as pd

# Sprawdź istnienie folderu "subtables" i utwórz go, jeśli nie istnieje
subtables_folder = "1subtables"
if not os.path.exists(subtables_folder):
    os.makedirs(subtables_folder)

# KROK 1 
# Utworzenie podtablic z reduktów
# Wczytaj plik CSV
df = pd.read_csv('modified_lymphography.csv')

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
    df_selected.to_csv(os.path.join(subtables_folder, f'modified_lymphography_reduct_subtable_{idx}.csv'), index=False)
