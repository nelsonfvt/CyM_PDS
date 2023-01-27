import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def sobel_edg(img):
    # Blur the image for better edge detection
    #img = cv.GaussianBlur(img, (3,3), 0) #Optional

    # Sobel Edge Detection
    sobelx = cv.Sobel(img, ddepth=cv.CV_64F, dx=1, dy=0) # default 3x3 kernel
    sobelx = np.absolute(sobelx)
    sobely = cv.Sobel(img, ddepth=cv.CV_64F, dx=0, dy=1)
    sobely = np.absolute(sobely)
    sobelxy = cv.Sobel(img, ddepth=cv.CV_64F, dx=1, dy=1)
    sobelxy = np.absolute(sobelxy)

    plt.subplot(2,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(2,2,2)
    plt.imshow(sobelxy,'gray')
    plt.title('Sobel XY')
    plt.subplot(2,2,3)
    plt.imshow(sobelx,'gray')
    plt.title('Sobel X')
    plt.subplot(2,2,4)
    plt.imshow(sobely,'gray')
    plt.title('Sobel Y')

    plt.show()

def Laplace_edg(img):
    # Blur the image for better edge detection
    #img = cv.GaussianBlur(img, (3,3), 0) #Optional

    lap = cv.Laplacian(img,cv.CV_64F)
    lap = np.absolute(lap)

    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(lap,'gray')
    plt.title('Laplaciano')
    plt.show()

def Canny_edg(img):
    cann = cv.Canny(img, 100, 200)
    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(cann,'gray')
    plt.title('Canny detection')
    plt.show()

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

sobel_edg(imagN)
sobel_edg(imagS)

Laplace_edg(imagN)
Laplace_edg(imagS)

Canny_edg(imagN)
Canny_edg(imagS)