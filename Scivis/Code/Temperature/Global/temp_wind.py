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

global_min_temp = float('inf')
global_max_temp = float('-inf')

# Dates to plot
dates_to_plot = ['2019-07-01', '2019-07-21', '2019-07-22', '2019-07-23', '2019-08-01', '2019-09-15']

for date in dates_to_plot:
    target_date = datetime.strptime(date, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    date = cftime.date2num(target_date, units=units, calendar=calendar)

    temp_day = tmmx['air_temperature'].sel(day=date)
    day_min = np.nanmin(temp_day)
    day_max = np.nanmax(temp_day)
    global_min_temp = min(global_min_temp, day_min)
    global_max_temp = max(global_max_temp, day_max)

def plot_wind_and_temp_for_day(day_to_plot):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS)
    target_date = datetime.strptime(day_to_plot, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day = cftime.date2num(target_date, units=units, calendar=calendar)

    wind_speed_day = wind_ft['wind_speed'].sel(day=day)
    wind_direction_day = wind_ft['wind_from_direction'].sel(day=day)

    temp_day = tmmx['air_temperature'].sel(day=day)

    valid_mask = ~np.isnan(wind_speed_day) & ~np.isnan(wind_direction_day)
    lat_values = wind_speed_day.lat.values
    lon_values = wind_speed_day.lon.values
    valid_lats, valid_lons = np.meshgrid(lat_values, lon_values, indexing='ij')

    lon_valid = valid_lons[valid_mask]
    lat_valid = valid_lats[valid_mask]
    wind_speed_valid = wind_speed_day.values[valid_mask]
    wind_direction_valid = wind_direction_day.values[valid_mask]

    lon_grid = np.linspace(lon_valid.min(), lon_valid.max(), 30) # 30 points in longitude range
    lat_grid = np.linspace(lat_valid.min(), lat_valid.max(), 25) # 25 points in longitude range
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

    temp_contour = ax.contourf(
        lon_grid, lat_grid, temp_grid, cmap='hot', alpha=0.6,
        levels=np.linspace(global_min_temp, global_max_temp, 30),
        vmin=global_min_temp, vmax=global_max_temp
    )

    cbar = plt.colorbar(temp_contour, ax=ax, orientation='vertical', label='Temperature (°C)')
    cbar.set_ticks(np.linspace(global_min_temp, global_max_temp, num=5))
    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    plt.title(f'Wind Speed and Temperature on {day_to_plot}')
    plt.savefig(f"temp_wind_plot_{day_to_plot}.png", dpi=100)
    plt.show()
    plt.close()

for date in dates_to_plot:
    plot_wind_and_temp_for_day(date)

print("Plots saved successfully.")
