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


vs = xr.open_dataset("../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../Dataset/2019/th_2019.nc",decode_times=False)
tmmx = xr.open_dataset("../../Dataset/2019/tmmx_2019.nc",decode_times=False)
# here pdsi* means the specific date and month of pdsi dataset
pdsi0701 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190701.nc",decode_times=False)
pdsi0720 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190720.nc",decode_times=False)
pdsi0801 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190801.nc",decode_times=False)
pdsi0820 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190820.nc",decode_times=False)
pdsi0901 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190901.nc",decode_times=False)
pdsi0920 = xr.open_dataset("../../Dataset/2019/permanent_gridmetPDSI_20190920.nc",decode_times=False)

wind_ft = xr.merge([vs, th])

def drought_plot(day, pdsi_data, temp_data, wind_data, filename):
    
    target_date = datetime.strptime(day, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day_to_plot = cftime.date2num(target_date, units=units, calendar=calendar)

    selected_day = temp_data.sel(day=day_to_plot, method='nearest')
    pdsi_selected = pdsi_data['palmer_drought_severity_index'].squeeze()
    wind_speed_day = wind_data['wind_speed'].sel(day=day_to_plot, method='nearest')
    wind_direction_day = wind_data['wind_from_direction'].sel(day=day_to_plot, method='nearest')

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)

    pdsi_plot = ax.imshow(
        pdsi_selected,
        extent=[pdsi_data['lon'].min(), pdsi_data['lon'].max(),
                pdsi_data['lat'].min(), pdsi_data['lat'].max()],
        origin='upper',
        cmap='BrBG', # set color
        alpha=0.8,
        transform=ccrs.PlateCarree()
    )

    temp_min = 260  # Set manually by preprocessing and plotting maps
    temp_max = selected_day['air_temperature'].max().values
    temp_contour = ax.contourf(
        selected_day['lon'], selected_day['lat'],
        selected_day['air_temperature'],
        levels=15, cmap='coolwarm', vmin=temp_min, vmax=temp_max,
        alpha=0.5, transform=ccrs.PlateCarree()
    )

    valid_mask = ~np.isnan(wind_speed_day) & ~np.isnan(wind_direction_day)
    lat_values = wind_speed_day.lat.values
    lon_values = wind_speed_day.lon.values
    valid_lats, valid_lons = np.meshgrid(lat_values, lon_values, indexing='ij')
    lon_valid = valid_lons[valid_mask]
    lat_valid = valid_lats[valid_mask]
    wind_speed_valid = wind_speed_day.values[valid_mask]
    wind_direction_valid = wind_direction_day.values[valid_mask]

    lon_min = wind_data['lon'].values.min()
    lon_max = wind_data['lon'].values.max()
    lon_grid = np.linspace(lon_min, lon_max, 40)
    lat_min = wind_data['lat'].values.min()
    lat_max = wind_data['lat'].values.max()
    lat_grid = np.linspace(lat_min, lat_max, 35)

    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')
    u = grid_speed * np.cos(np.deg2rad(grid_direction))
    v = grid_speed * np.sin(np.deg2rad(grid_direction))

    ax.streamplot(lon_grid, lat_grid, u, v, color='darkblue', linewidth=0.5, density=1, transform=ccrs.PlateCarree())

    cbar_pdsi = fig.colorbar(pdsi_plot, ax=ax, label='Palmer Drought Severity Index (PDSI)')
    cbar_temp = fig.colorbar(temp_contour, ax=ax, label='Average Temperature (K)')
    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    ax.set_title(f"Drought Conditions on {day}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.savefig(filename, bbox_inches='tight',dpi=200)
    plt.show()

dates = [pdsi0701, pdsi0720, pdsi0801, pdsi0820, pdsi0901, pdsi0920]
dates1 = ['2019-07-01', '2019-07-20', '2019-08-01', '2019-08-20', '2019-09-01', '2019-09-20']

for i in range(len(dates)):
    drought_plot(dates1[i], dates[i], tmmx, wind_ft, f'drought_plot_{dates1[i]}.png')