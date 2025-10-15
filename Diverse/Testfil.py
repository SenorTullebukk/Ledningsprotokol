import pandas as pd
import itertools

df = pd.read_excel('Diverse/SepterFil.xlsx')

import matplotlib.pyplot as plt

# Extract the string of coordinates and plot lines with same level in same color

level_colors = {}  # Map level to color
color_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

for idx, row in df.iterrows():
    coords_str = row['Vertices']
    level = row.get('Level', None)  # Adjust 'Level' to your actual column name
    if level not in level_colors:
        level_colors[level] = next(color_cycle)
    color = level_colors[level]

    coords = coords_str.split(';')
    x, y, z = [], [], []
    for coord in coords:
        coord = coord.strip().replace('(', '').replace(')', '')
        if coord:
            parts = coord.split(',')
            x.append(float(parts[0]))
            y.append(float(parts[1]))
    plt.plot(x, y, label=f'Row {idx} (Level {level})', color=color)
plt.show()
