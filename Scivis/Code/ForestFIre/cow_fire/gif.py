from PIL import Image
import imageio.v2 as imageio
import numpy as np

# cowfire plot continuous

frame1 = Image.open('cow_wildfire_plot_2019-07-20.png')
frame2 = Image.open('cow_wildfire_plot_2019-07-22.png')
frame3 = Image.open('cow_wildfire_plot_2019-07-24.png')
frame4 = Image.open('cow_wildfire_plot_2019-07-27.png')
frame5 = Image.open('cow_wildfire_plot_2019-08-05.png')
frame6 = Image.open('cow_wildfire_plot_2019-09-01.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('cow_wildfire.gif', images, duration=2)