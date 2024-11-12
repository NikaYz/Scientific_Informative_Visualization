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


def plot_wind_for_day(day):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())  # Set extent once
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS)

    target_date = datetime.strptime(day, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day_to_plot = cftime.date2num(target_date, units=units, calendar=calendar)

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
    lon_min, lon_max = wind_ft['lon'].min().values, wind_ft['lon'].max().values
    lat_min, lat_max = wind_ft['lat'].min().values, wind_ft['lat'].max().values

    lon_grid = np.linspace(lon_min, lon_max, 40)  # 40 points in longitude range
    lat_grid = np.linspace(lat_min, lat_max, 35)  # 30 points in latitude range
    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)
    min_wind_speed = wind_speed_valid.min()
    max_wind_speed = wind_speed_valid.max()
    num_categories = 20 # can change accordingly to bins required in colormap
    categories = np.linspace(min_wind_speed, max_wind_speed, num_categories + 1)  # Create edges for 20 bins

    viridis = cm.get_cmap('viridis', num_categories)
    colors = viridis(np.linspace(0, 1, num_categories))

    cmap = ListedColormap(colors)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')

    vmin = wind_speed_day.min().values
    vmax = wind_speed_day.max().values*0.75

    norm = Normalize(vmin=vmin, vmax=vmax)
    arrow_colors = plt.cm.viridis(norm(grid_speed))

    arrow_colors = np.dstack([arrow_colors[:, :, :3], np.ones_like(grid_speed)])

    u = np.cos(np.deg2rad(grid_direction))
    v = np.sin(np.deg2rad(grid_direction))

    q = ax.quiver(
        lon_grid, lat_grid, u, v,
        color=arrow_colors.reshape(-1, 4),
        scale_units='xy',
        scale= 1  # Adjust the scale
    )

    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical')
    cbar.set_label('Wind Speed (m/s)')
    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    plt.title(f'Wind Speed and Direction on {day}')
    plt.savefig(f'wind_plot_{day}', bbox_inches='tight', dpi=100)

dates_to_plot = ['2019-07-01', '2019-07-15', '2019-08-01', '2019-08-15', '2019-09-01', '2019-09-15']

for i in range(len(dates_to_plot)):
    plot_wind_for_day(dates_to_plot[i])


#plt.show()