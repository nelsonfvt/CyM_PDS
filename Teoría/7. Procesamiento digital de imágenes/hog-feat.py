import cv2 as cv
import numpy as np
from skimage import feature
from matplotlib import pyplot as plt

def hog_feature(img):
    (hog,hog_image) = feature.hog(img, orientations = 9, pixels_per_cell = (8,8), cells_per_block = (3,3), block_norm = 'L2-Hys', visualize = True, transform_sqrt = True)
    print(hog[0])
    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(hog_image,'gray')
    plt.title('HOG Image')
    plt.show()

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

hog_feature(imagN)
hog_feature(imagS)