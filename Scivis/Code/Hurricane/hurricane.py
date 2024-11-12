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


vs = xr.open_dataset("../../Dataset/2019/vs_2019.nc",decode_times=False)
th = xr.open_dataset("../../Dataset/2019/th_2019.nc",decode_times=False)
pr = xr.open_dataset("../../Dataset/2019/pr_2019.nc",decode_times=False)
sph = xr.open_dataset("../../Dataset/2019/sph_2019.nc",decode_times=False)

wind_ft = xr.merge([vs, th])

def plot_affected_area(ax, center_lat, center_lon, radius_lat, radius_lon, color='yellow'):
    ellipse = Ellipse(
        xy=(center_lon, center_lat),
        width=2*radius_lon, height=2*radius_lat,
        edgecolor='black', facecolor=color, alpha=0.5
    )
    ax.add_patch(ellipse)

def combined_plot(day, wind_ft, pr, sph, filename,t):

    target_date = datetime.strptime(day, "%Y-%m-%d")
    units = "days since 1900-01-01 00:00:00"
    calendar = "gregorian"
    day_to_plot = cftime.date2num(target_date, units=units, calendar=calendar)
    wind_speed_day = wind_ft['wind_speed'].sel(day=day_to_plot)
    wind_direction_day = wind_ft['wind_from_direction'].sel(day=day_to_plot)
    precipitation_day = pr['precipitation_amount'].sel(day=day_to_plot)
    humidity_day = sph['specific_humidity'].sel(day=day_to_plot)

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-95, -85, 25, 35], crs=ccrs.PlateCarree()) # zoom extent to observe designated area
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)

    valid_mask = ~np.isnan(wind_speed_day) & ~np.isnan(wind_direction_day)
    lat_values = wind_speed_day.lat.values
    lon_values = wind_speed_day.lon.values
    valid_lats, valid_lons = np.meshgrid(lat_values, lon_values, indexing='ij')
    lon_valid = valid_lons[valid_mask]
    lat_valid = valid_lats[valid_mask]
    wind_speed_valid = wind_speed_day.values[valid_mask]
    wind_direction_valid = wind_direction_day.values[valid_mask]

    lon_min = wind_ft['lon'].values.min()
    lon_max = wind_ft['lon'].values.max()
    lon_grid = np.linspace(lon_min, lon_max, 40)
    lat_min = wind_ft['lat'].values.min()
    lat_max = wind_ft['lat'].values.max()
    lat_grid = np.linspace(lat_min, lat_max, 35)

    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    grid_speed = griddata((lon_valid, lat_valid), wind_speed_valid, (lon_grid, lat_grid), method='linear')
    grid_direction = griddata((lon_valid, lat_valid), wind_direction_valid, (lon_grid, lat_grid), method='linear')
    u = grid_speed * np.cos(np.deg2rad(grid_direction))
    v = grid_speed * np.sin(np.deg2rad(grid_direction))

    ax.streamplot(lon_grid, lat_grid, u, v, color='darkblue', linewidth=0.5, density=1, transform=ccrs.PlateCarree())

    precip_min = precipitation_day.min().values
    precip_max = precipitation_day.max().values
    precipitation_contour = ax.contourf(
        precipitation_day['lon'], precipitation_day['lat'],
        precipitation_day,
        levels=15,
        cmap='Blues',
        vmin=precip_min,
        vmax=precip_max,
        alpha=0.6,
        transform=ccrs.PlateCarree()
    )

    humidity_plot = ax.imshow(
        humidity_day,
        extent=[sph['lon'].min(), sph['lon'].max(),
                sph['lat'].min(), sph['lat'].max()],
        origin='upper',
        cmap='YlGnBu',
        alpha=0.6,
        transform=ccrs.PlateCarree()
    )

    cbar_precip = fig.colorbar(precipitation_contour, ax=ax, label='Precipitation (mm)')
    cbar_humidity = fig.colorbar(humidity_plot, ax=ax, label='Specific Humidity (kg/kg)')
    gl = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    ax.set_title(f"Hurricane Barry on {day} ({t})")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Plot the affected areas at each stage of the hurricane
    # Initial Formation Stage (July 10, 2019)
    if day == '2019-07-10':
        plot_affected_area(ax, 25.0, -85.0, 2.0, 2.5, color='yellow')

    # Tropical Storm Stage (July 11, 2019)
    elif day == '2019-07-11':
        plot_affected_area(ax, 27.0, -87.5, 3.0, 3.5, color='orange')

    # Intensification Phase (July 12, 2019)
    elif day == '2019-07-12':
        plot_affected_area(ax, 28.5, -90.0, 4.0, 4.5, color='red')

    # Landfall (July 13, 2019)
    elif day == '2019-07-13':
        plot_affected_area(ax, 29.0, -90.5, 5.0, 5.5, color='darkred')

    # Post-Landfall Weakening (July 14, 2019)
    elif day == '2019-07-14':
        plot_affected_area(ax, 30.0, -91.5, 6.0, 6.5, color='purple')

    # Dissipation (July 15, 2019)
    elif day == '2019-07-15':
        plot_affected_area(ax, 31.5, -93.0, 7.0, 7.5, color='yellow')

    plt.savefig(filename, bbox_inches='tight', dpi=200)
    #plt.show()

dates = ['2019-07-10', '2019-07-11', '2019-07-12', '2019-07-13', '2019-07-14', '2019-07-15']
terms = ['Initial Formation Stage','Tropical Storm Stage','Intensification Phase','Landfall', 'Post-Landfall Weakening','Dissipation']
for i in range (len(dates)):
    combined_plot(dates[i], wind_ft, pr, sph, f'hurricane_plot_{dates[i]}.png',terms[i])
