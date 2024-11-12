
from PIL import Image
import imageio.v2 as imageio
import numpy as np

# walker wildfire plot continuous

frame1 = Image.open('walker_wildfire_plot_2019-08-29.png')
frame2 = Image.open('walker_wildfire_plot_2019-09-01.png')
frame3 = Image.open('walker_wildfire_plot_2019-09-03.png')
frame4 = Image.open('walker_wildfire_plot_2019-09-06.png')
frame5 = Image.open('walker_wildfire_plot_2019-09-15.png')
frame6 = Image.open('walker_wildfire_plot_2019-09-25.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('walker_wildfire.gif', images, duration=2)