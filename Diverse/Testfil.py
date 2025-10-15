import pandas as pd
import itertools

df = pd.read_excel('Diverse/SepterFil3.xlsx')

import matplotlib.pyplot as plt

# Extract the string of coordinates and plot lines with same level in same color

print(df.loc[0])
'''
level_colors = {}  # Map level to color
color_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

for idx, row in df.iterrows():
    coords_str = row['Vertices']
    level = row.get('Level', None)  # Adjust 'Level' to your actual column name
    if level != "TV_U_APT_SSkrm":
        continue  # Skip rows not matching the desired level
    if level not in level_colors:
        level_colors[level] = next(color_cycle)
    color = level_colors[level]

    coords = coords_str.split(';')
    x, y, z = [], [], []
    for coord in coords:
        coord = coord.strip().replace('(', '').replace(')', '')
        if coord:
            parts = coord.split(',')
            if len(parts) >= 2:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
    plt.plot(x, y, label=f'Row {idx} (Level {level})', color=color)
plt.show()
'''