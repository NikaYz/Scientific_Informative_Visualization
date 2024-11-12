from PIL import Image
import imageio.v2 as imageio
import numpy as np

from PIL import Image
import imageio.v2 as imageio
import numpy as np

frame1 = Image.open('wind_plot_black_2019-07-01.png')
frame2 = Image.open('wind_plot_black_2019-07-15.png')
frame3 = Image.open('wind_plot_black_2019-08-01.png')
frame4 = Image.open('wind_plot_black_2019-08-15.png')
frame5 = Image.open('wind_plot_black_2019-09-01.png')
frame6 = Image.open('wind_plot_black_2019-09-15.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('wind_plot_black.gif', images, duration=1)