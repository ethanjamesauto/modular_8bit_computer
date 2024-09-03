import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
img = Image.open("img.ppm")
plt.imshow(img)
plt.show()