from PIL import Image
import imageio.v2 as imageio
import numpy as np

frame1 = Image.open('wind_streamlines_2019-07-01_lightblue.png')
frame2 = Image.open('wind_streamlines_2019-07-15_lightblue.png')
frame3 = Image.open('wind_streamlines_2019-08-01_lightblue.png')
frame4 = Image.open('wind_streamlines_2019-08-15_lightblue.png')
frame5 = Image.open('wind_streamlines_2019-09-01_lightblue.png')
frame6 = Image.open('wind_streamlines_2019-09-15_lightblue.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('streamline_plot_lightblue.gif', images, duration=2)