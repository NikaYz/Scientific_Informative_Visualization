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

vs = xr.open_dataset("../../../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../../../Dataset/2019/th_2019.nc",decode_times=False)

wind_ft = xr.merge([vs, th])

# can cahnge colormap of this as required
cmap = cm.viridis
norm = Normalize(vmin=0, vmax=7)  # Set a limit manually by preprocessing and plotting maps

mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])

def plot_wind_for_day(day):
    
    target_date = datetime.strptime(day, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day_to_plot = cftime.date2num(target_date, units=units, calendar=calendar)
    
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())  # Set extent once
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS)

    wind_speed_day = wind_ft['wind_speed'].sel(day=day_to_plot)
    wind_direction_day = wind_ft['wind_from_direction'].sel(day=day_to_plot)

    valid_mask = ~np.isnan(wind_speed_day) & ~np.isnan(wind_direction_day)
    lat_values = wind_speed_day.lat.values
    lon_values = wind_speed_day.lon.values
    valid_lats, valid_lons = np.meshgrid(lat_values, lon_values, indexing='ij')

    lon_valid = valid_lons[valid_mask]
    lat_valid = valid_lats[valid_mask]
    wind_speed_valid = wind_speed_day.values[valid_mask]
    wind_direction_valid = wind_direction_day.values[valid_mask]

    lon_grid = np.linspace(lon_valid.min(), lon_valid.max(), 40) # 40 points in longitude range
    lat_grid = np.linspace(lat_valid.min(), lat_valid.max(), 25) # 25 points in latitude range
    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')

    u = np.cos(np.deg2rad(grid_direction))
    v = np.sin(np.deg2rad(grid_direction))

    arrow_colors = mappable.to_rgba(grid_speed)

    ax.quiver(
        lon_grid, lat_grid, u, v,
        color=arrow_colors.reshape(-1, 4),
        scale=50 # Set scale accordingly
    )

    
    cbar = plt.colorbar(mappable, ax=ax, orientation='vertical')
    cbar.set_label('Wind Speed (m/s)')
    ax.cbar = cbar

    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    ax.set_title(f'Wind Speed and Direction on {day}')
    plt.savefig(f"wind_plot_{day}.png", dpi=200)

dates_to_plot = ['2019-07-01', '2019-07-15', '2019-08-01', '2019-08-15', '2019-09-01', '2019-09-15']


for i in range(len(dates_to_plot)):
    plot_wind_for_day(dates_to_plot[i])

plt.show()