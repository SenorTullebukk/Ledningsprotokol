import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f"Clicked coordinates: ({event.xdata:.2f}, {event.ydata:.2f})")

fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set extent to Denmark
ax.set_extent([7.5, 13.0, 54.5, 58.0], crs=ccrs.PlateCarree())

ax.set_title("Click on the map to get coordinates")
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAKES, facecolor='lightblue')
ax.add_feature(cfeature.RIVERS)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        coords = f"{event.xdata:.6f}, {event.ydata:.6f}"
        print(f"Clicked coordinates: ({coords})")

plt.show()