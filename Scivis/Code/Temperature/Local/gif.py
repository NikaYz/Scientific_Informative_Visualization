from PIL import Image
import imageio.v2 as imageio
import numpy as np

# temperature and wind plot global

frame1 = Image.open('temp_wind_plot_2019-07-01_local.png')
frame2 = Image.open('temp_wind_plot_2019-07-21_local.png')
frame3 = Image.open('temp_wind_plot_2019-07-22_local.png')
frame4 = Image.open('temp_wind_plot_2019-07-23_local.png')
frame5 = Image.open('temp_wind_plot_2019-08-01_local.png')
frame6 = Image.open('temp_wind_plot_2019-09-15_local.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('wind_temperature_local.gif', images, duration=2)