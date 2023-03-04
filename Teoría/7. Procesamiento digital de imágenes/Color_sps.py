import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def RGB_HSV (imag):
    i_hsv = cv.cvtColor(imag, cv.COLOR_BGR2HSV)
    plot_imags(imag, i_hsv)
    

def RGB_LAB(imag):
    i_lab = cv.cvtColor(imag, cv.COLOR_BGR2Lab)
    plot_imags(imag, i_lab)
    

def split_channs(imag):
    C1, C2, C3 = cv.split(imag)
    # plt.subplot(3,1,1)
    # plt.imshow(C1, 'gray')
    # plt.subplot(3,1,2)
    # plt.imshow(C2, 'gray')
    # plt.subplot(3,1,3)
    # plt.imshow(C3, 'gray')
    # plt.show()
    
def plot_imags(original, transformada):
    plt.subplot(1,2,1)
    plt.imshow(original, 'gray')
    plt.subplot(1,2,2)
    plt.imshow(transformada, 'gray')
    plt.show()

imagN = cv.imread('imag1.jpg') # CARGANDO IMAGEN NATURAL BGR
imagS = cv.imread('dibujo.png') # CARGANDO IMAGEN SINTÉTICA BGR

RGB_imagN = cv.cvtColor(imagN, cv.COLOR_BGR2RGB) #BGR -> RGB
RGB_imagS = cv.cvtColor(imagS, cv.COLOR_BGR2RGB) #BGR -> RGB

plot_imags(imagN, RGB_imagN)
plot_imags(imagS, RGB_imagS)

#imagen a HSV
RGB_HSV(RGB_imagN)
RGB_HSV(RGB_imagS)

#imagen a L*a*b*
RGB_LAB(RGB_imagN)
RGB_LAB(RGB_imagS)