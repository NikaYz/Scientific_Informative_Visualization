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
import matplotlib.patches as patches
import cftime
from datetime import datetime

#this is used used to bypass SSL certificate verification when making HTTPS requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


vs = xr.open_dataset("../../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../../Dataset/2019/th_2019.nc",decode_times=False)
vpd = xr.open_dataset("../../../Dataset/2019/vpd_2019.nc",decode_times=False)
fm100 = xr.open_dataset("../../../Dataset/2019/fm100_2019.nc",decode_times=False)

wind_ft = xr.merge([vs, th])
def forestfire_plot(day_to_plot,d):
    target_date = datetime.strptime(day_to_plot, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day = cftime.date2num(target_date, units=units, calendar=calendar)

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-125, -115, 35, 40], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS)

    selected_vpd = vpd.sel(day=day)
    vpd_contour = ax.contourf(
        selected_vpd['lon'], selected_vpd['lat'],
        selected_vpd['mean_vapor_pressure_deficit'],
        transform=ccrs.PlateCarree(),
        cmap='OrRd',
        alpha=0.5,
        levels=20
    )

    selected_fm = fm100.sel(day=day)
    fm_image = ax.imshow(
        selected_fm['dead_fuel_moisture_100hr'],
        extent=[selected_fm['lon'].min(), selected_fm['lon'].max(),
                selected_fm['lat'].min(), selected_fm['lat'].max()],
        origin='upper',
        cmap='Greens',
        alpha=0.6,
        transform=ccrs.PlateCarree()
    )

    wind_speed_day = wind_ft['wind_speed'].sel(day=day)
    wind_direction_day = wind_ft['wind_from_direction'].sel(day=day)

    lat_indices = np.linspace(0, len(wind_speed_day['lat']) - 1, 50, dtype=int) # 50 points in latitude range
    lon_indices = np.linspace(0, len(wind_speed_day['lon']) - 1, 75, dtype=int) # 75 points in longitude range

    u = np.cos(np.deg2rad(wind_direction_day[lat_indices, :][:, lon_indices])) * wind_speed_day[lat_indices, :][:, lon_indices]
    v = np.sin(np.deg2rad(wind_direction_day[lat_indices, :][:, lon_indices])) * wind_speed_day[lat_indices, :][:, lon_indices]

    lon_grid, lat_grid = np.meshgrid(wind_speed_day['lon'][lon_indices], wind_speed_day['lat'][lat_indices])

    ax.quiver(lon_grid, lat_grid, u, v, scale=70, color='black', alpha=0.6)

    #Here one can comment down the respective coordinates and polygon creation for respective wildfire visualization (can alternatively change between two)

    cow_fire_coords = [(-119.7, 35.5), (-119.7, 35.4), (-119.5, 35.4), (-119.5, 35.5)]
    #walker_fire_coords = [(-120.5, 39.4), (-120.5, 39.3), (-120.3, 39.3), (-120.3, 39.4)]

    # Create polygons for the fire-affected areas  (can alternatively change between two)

    cow_fire_poly = patches.Polygon(cow_fire_coords, closed=True, color='blue', alpha=1, label='Cow Fire')
    ax.add_patch(cow_fire_poly)

    #walker_fire_poly = patches.Polygon(walker_fire_coords, closed=True, color='yellow', alpha=1, label='Walker Fire')
    #ax.add_patch(walker_fire_poly)

    cbar_vpd = fig.colorbar(vpd_contour, ax=ax, orientation="vertical", fraction=0.03, pad=0.1)
    cbar_vpd.set_label("Vapor Pressure Deficit (hPa)", labelpad=5)

    cbar_fm = fig.colorbar(fm_image, ax=ax, orientation="vertical", fraction=0.03, pad=0.1)
    cbar_fm.set_label("Dead Fuel Moisture (%)", labelpad=5)

    plt.title(f"Cow Wildfire Plot for {day_to_plot} ({d})")
    gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray")
    gl.top_labels = gl.right_labels = False

    ax.legend()
    plt.savefig(f"cow_wildfire_plot_{day_to_plot}.png", dpi=50)
    #plt.show()

dates_to_plot = ['2019-07-01', '2019-07-15', '2019-08-01', '2019-08-15', '2019-09-01', '2019-09-15','2019-09-30']
cowFireDates = [
    "2019-07-20", # 5 days before
    "2019-07-22", # 3 days before
    "2019-07-24", # 1 day before
    "2019-07-27", # 2 days after
    "2019-08-05", # 1 week after
    "2019-09-01"  # 1 month after
]
days = [
    "5 days before",
   "3 days before",
    "1 day before",
    "2 days after",
    "1 week after",
    "1 month after"]
# Loop over each date and generate the plot
for i in range(len(days)):
    forestfire_plot(cowFireDates[i], days[i])