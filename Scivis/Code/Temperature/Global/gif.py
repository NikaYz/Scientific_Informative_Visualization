from PIL import Image
import imageio.v2 as imageio
import numpy as np

frame1 = Image.open('temp_wind_plot_2019-07-01.png')
frame2 = Image.open('temp_wind_plot_2019-07-21.png')
frame3 = Image.open('temp_wind_plot_2019-07-22.png')
frame4 = Image.open('temp_wind_plot_2019-07-23.png')
frame5 = Image.open('temp_wind_plot_2019-08-01.png')
frame6 = Image.open('temp_wind_plot_2019-09-15.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('wind_temperature_global.gif', images, duration=2)