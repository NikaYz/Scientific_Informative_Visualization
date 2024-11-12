from PIL import Image
import imageio.v2 as imageio
import numpy as np
# used different approach here since it shows error for different sizes of images(thanks to stackoverflow for the suggestion to use Image.LANCZOS)
fixed_size = (1400, 800)
image_paths = [
    'drought_plot_2019-07-01.png',
    'drought_plot_2019-07-20.png',
    'drought_plot_2019-08-01.png',
    'drought_plot_2019-08-20.png',
    'drought_plot_2019-09-01.png',
    'drought_plot_2019-09-20.png'
]

images = []

for file in image_paths:
    with Image.open(file) as img:
        img_r = img.resize(fixed_size, Image.LANCZOS)
        images.append(np.array(img_r))


imageio.mimsave('drought.gif', images, duration=2)