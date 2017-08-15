import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


##images = sorted(os.listdir(self._img_file))
##imgpath = self._img_file + images[-1]
## data = 'Pitch: 0.189\n Roll: -0.021' ## Placeholder for IMU Data

def update_image(imgpath, data = None):
    """Receives path/to/image and IMU data, then updates displayed output"""
    img = mpimg.imread(imgpath)
    plt.imshow(img)
    if data:
        txt = 'Pitch: ' + data[0] + '\n' + 'Roll: ' + data[1]
        overlay = plt.text(310, 50, txt, horizontalalignment='right', color='white')
    plt.axis('off')
    plt.draw()
    plt.show()
