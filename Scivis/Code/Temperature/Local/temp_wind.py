from matplotlib.quiver import Quiver
# importing required functions to implement scivis
import pandas as pd
import xarray as xr
import dask.array as da
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature
from matplotlib.colors import Normalize,  ListedColormap
import matplotlib.cm as cm
from scipy.interpolate import griddata
import matplotlib.quiver as mquiver
import matplotlib.animation as animation
import imageio
from PIL import Image
import cartopy.feature as cfeature
#this is used used to bypass SSL certificate verification when making HTTPS requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import cftime
from datetime import datetime
from matplotlib.patches import Ellipse
from matplotlib.quiver import Quiver
from matplotlib import contour


vs = xr.open_dataset("../../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../../Dataset/2019/th_2019.nc",decode_times=False)
tmmx = xr.open_dataset("../../../Dataset/2019/tmmx_2019.nc",decode_times=False)

wind_ft = xr.merge([vs, th])

def plot_wind_and_temp_for_day(day, ax, cbar=None):
    target_date = datetime.strptime(day, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day_to_plot = cftime.date2num(target_date, units=units, calendar=calendar)

    for artist in ax.get_children():
        if isinstance(artist, Quiver):
            artist.remove()
        elif isinstance(artist, contour.QuadContourSet):
            artist.remove()

    wind_speed_day = wind_ft['wind_speed'].sel(day=day_to_plot)
    wind_direction_day = wind_ft['wind_from_direction'].sel(day=day_to_plot)

    temp_day = tmmx['air_temperature'].sel(day=day_to_plot)

    valid_mask = ~np.isnan(wind_speed_day) & ~np.isnan(wind_direction_day)
    lat_values = wind_speed_day.lat.values
    lon_values = wind_speed_day.lon.values
    valid_lats, valid_lons = np.meshgrid(lat_values, lon_values, indexing='ij')

    lon_valid = valid_lons[valid_mask]
    lat_valid = valid_lats[valid_mask]
    wind_speed_valid = wind_speed_day.values[valid_mask]
    wind_direction_valid = wind_direction_day.values[valid_mask]

    lon_grid = np.linspace(lon_valid.min(), lon_valid.max(), 30) # 30 points in longitude range
    lat_grid = np.linspace(lat_valid.min(), lat_valid.max(), 25) # 25 points in latitude range
    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')

    u = grid_speed * np.cos(np.deg2rad(grid_direction))
    v = grid_speed * np.sin(np.deg2rad(grid_direction))

    ax.quiver(
        lon_grid, lat_grid, u, v,
        color='black',  # Set the color of all arrows to black
        scale=150 # Set scale as required
    )

    temp_valid_mask = ~np.isnan(temp_day)
    temp_grid = griddata((lon_valid, lat_valid), temp_day.values[temp_valid_mask], (lon_grid, lat_grid), method='linear')

    temp_contour = ax.contourf(lon_grid, lat_grid, temp_grid, cmap='hot', alpha=0.5, levels=15)

    if cbar is None:
        cbar = plt.colorbar(temp_contour, ax=ax, orientation='vertical', label='Temperature (°C)')
    else:
        cbar.ax.clear()
        cbar = plt.colorbar(temp_contour, cax=cbar.ax, orientation='vertical', label='Temperature (°C)')

    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    ax.set_title(f'Wind Speed and Temperature on {day}')
    plt.savefig(f"temp_wind_plot_{day}_local.png", dpi=100)
    return cbar

dates_to_plot = ['2019-07-01', '2019-07-21', '2019-07-22', '2019-07-23', '2019-08-01', '2019-09-15']
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS)

cbar = None

for i in range(len(dates_to_plot)):
    cbar = plot_wind_and_temp_for_day(dates_to_plot[i], ax, cbar)

plt.show()