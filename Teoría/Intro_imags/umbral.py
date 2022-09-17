import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def manual_thresh(img, trh):
    ret,thresh1 = cv.threshold(img,trh,255,cv.THRESH_BINARY)
    ret,thresh2 = cv.threshold(img,trh,255,cv.THRESH_BINARY_INV)
    ret,thresh3 = cv.threshold(img,trh,255,cv.THRESH_TRUNC)
    ret,thresh4 = cv.threshold(img,trh,255,cv.THRESH_TOZERO)
    ret,thresh5 = cv.threshold(img,trh,255,cv.THRESH_TOZERO_INV)
    titles = ['Imagen original','Binaria','Binaria invertida','Truncada','Hasta cero','Hasta cero invertida']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

def adap_thresh(img):
    img = img.astype(np.uint8)
    img = cv.medianBlur(img,5)
    ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
    th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in range(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

# Aplicando umbral manual
manual_thresh(imagN, 127)
manual_thresh(imagS, 127)

# Aplicando umbral adaptativo
adap_thresh(imagN)
adap_thresh(imagS)