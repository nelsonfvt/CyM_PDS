import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def RGB_HSV (imag):
    i_hsv = cv.cvtColor(imag, cv.COLOR_BGR2HSV)
    cv.imshow('Original', imag)
    cv.imshow('Imagen HSV', i_hsv)
    cv.waitKey(0)
    cv.destroyAllWindows()

def plot_imgs(imag1, imag2):
    plt.subplot(2,1,1)
    plt.imshow(imag1, 'gray')
    plt.subplot(2,1,2)
    plt.imshow(imag2,'gray')

imagN = cv.imread('imag1.jpg') # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png') # CARGANDO IMAGEN SINTÉTICA

RGB_HSV(imagN)
RGB_HSV(imagS)