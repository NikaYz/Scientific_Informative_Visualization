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


vs = xr.open_dataset("../../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../../Dataset/2019/th_2019.nc",decode_times=False)

wind_ft = xr.merge([vs, th])

def streamline_plot(day, filename):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

    ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())
    ax.coastlines()

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
    lat_grid = np.linspace(lat_min, lat_max, 35)   # 35 points in latitude range
    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')

    u = grid_speed * np.cos(np.deg2rad(grid_direction))
    v = grid_speed * np.sin(np.deg2rad(grid_direction))

    strm = ax.streamplot(
        lon_grid, lat_grid, u, v,
        color='lightblue',
        linewidth=1,
        density=2
    )

    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    plt.title(f'Wind Streamlines and Speed on {day}')
    plt.savefig(filename, bbox_inches='tight', dpi=100)
    plt.show()

dates = ['2019-07-01', '2019-07-15', '2019-08-01','2019-08-15','2019-09-01', '2019-09-15']
for date in dates:
    streamline_plot(date, f'wind_streamlines_{date}_lightblue.png')