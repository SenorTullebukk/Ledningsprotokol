import geopandas as gpd
import matplotlib.pyplot as plt

# Read DXF file (ensure the file exists and drivers are installed)

gdf = gpd.read_file('Diverse/SomDXF.dxf')
# Print available columns to inspect

center = gdf.geometry.centroid.unary_union.centroid
gdf['distance'] = gdf.geometry.distance(center)
gdf = gdf[gdf['distance'] <= 5000]
print(gdf.columns)

# Plot features color-coded by 'Layer'
gdf.plot(column='Layer', legend=True)
plt.show()