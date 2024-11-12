from PIL import Image
import imageio.v2 as imageio
import numpy as np

# making gif for  hurricane Barry
frame1 = Image.open('hurricane_plot_2019-07-10.png')
frame2 = Image.open('hurricane_plot_2019-07-11.png')
frame3 = Image.open('hurricane_plot_2019-07-12.png')
frame4 = Image.open('hurricane_plot_2019-07-13.png')
frame5 = Image.open('hurricane_plot_2019-07-14.png')
frame6 = Image.open('hurricane_plot_2019-07-15.png')

images = [np.array(frame) for frame in [frame1, frame2, frame3, frame4, frame5, frame6]]

imageio.mimsave('hurricane_Barry.gif', images, duration=2)