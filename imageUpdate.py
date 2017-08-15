import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


images = sorted(os.listdir(self._img_file))
imgpath = self._img_file + images[-1]

txt = 'Pitch: 0.189\n Roll: -0.021' ## Placeholder for IMU Data

img = mpimg.imread(imgpath)
plt.imshow(img)
overlay = plt.text(310, 10, txt, horizontalalignment='right', color='white')
plt.axis('off')
plt.draw()
plt.show()
