from PIL import Image
import imageio.v2 as imageio
import numpy as np

# used different approach here since it shows error for different sizes of images(thanks to stackoverflow for the suggestion to use Image.LANCZOS)
fixed_size = (1400, 800)
images = []
image_paths = [
    'wind_plot_2019-07-01.png',
    'wind_plot_2019-07-15.png',
    'wind_plot_2019-08-01.png',
    'wind_plot_2019-08-15.png',
    'wind_plot_2019-09-01.png',
    'wind_plot_2019-09-15.png'
]
for file in image_paths:
    with Image.open(file) as img:
        img_r = img.resize(fixed_size, Image.LANCZOS)
        images.append(np.array(img_r))


imageio.mimsave('wind_plot_discrete_colormap.gif', images, duration=2)