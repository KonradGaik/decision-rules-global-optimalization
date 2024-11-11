import os
import pandas as pd

for x in range(1,6):
    print(x)
    if not os.path.exists(f'../RESULTS/subtable_{x}'):
        os.makedirs(f'../RESULTS/subtable_{x}')

# KROK 1 
# Utworzenie podtablic z reduktów
# Wczytaj plik CSV
df = pd.read_csv('../modified_tic-tac-toe.csv')

df = df[~df.apply(lambda row: all(value == 'c' for value in row), axis=1)]


reducts = [
    { 'top-left-square', 'top-middle-square', 'top-right-square', 'middle-left-square', 'middle-right-square', 'bottom-left-square', 'bottom-middle-square', 'bottom-right-square' },
    { 'top-left-square', 'top-middle-square', 'top-right-square', 'middle-left-square', 'middle-middle-square', 'middle-right-square', 'bottom-left-square', 'bottom-middle-square' },
    { 'top-left-square', 'top-middle-square', 'top-right-square', 'middle-left-square', 'middle-middle-square', 'middle-right-square', 'bottom-middle-square', 'bottom-right-square' },
    { 'top-left-square', 'top-middle-square', 'top-right-square', 'middle-left-square', 'middle-middle-square', 'bottom-left-square', 'bottom-middle-square', 'bottom-right-square' },
    { 'top-left-square', 'top-right-square', 'middle-left-square', 'middle-middle-square', 'middle-right-square', 'bottom-left-square', 'bottom-middle-square', 'bottom-right-square' }
]



for idx, reduct in enumerate(reducts, start=1):
    df_selected = df[list(reduct) + ['Class']]
    df_selected.to_csv(os.path.join(f'../RESULTS/subtable_{idx}', f'1tic_tac_toe_reduct_subtable_{idx}.csv'), index=False)
