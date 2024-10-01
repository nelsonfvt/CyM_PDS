import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import ctypes

def RGB_HSV (imag):
    i_hsv = cv.cvtColor(imag, cv.COLOR_BGR2HSV)
    plot_imags(imag, i_hsv, 'RGB', 'HSV') #mostrando imagenes
    split_channs(i_hsv, 'Hue', 'Saturation', 'Value') #Dividiendo canales
    
    

def RGB_LAB(imag):
    i_lab = cv.cvtColor(imag, cv.COLOR_BGR2Lab)
    plot_imags(imag, i_lab, 'RGB', 'L*a*b*') #mostrando imagenes
    split_channs(i_lab, 'L*', 'a*', 'b*') #Dividiendo canales

def split_channs(imag, t1='Canal 1', t2='Canal 2', t3='Canal 3'):
    C1, C2, C3 = cv.split(imag)
    plt.subplot(1,3,1)
    plt.imshow(C1, 'gray')
    plt.title(t1)
    plt.subplot(1,3,2)
    plt.imshow(C2, 'gray')
    plt.title(t2)
    plt.subplot(1,3,3)
    plt.imshow(C3, 'gray')
    plt.title(t3)
    plt.show()
    
def plot_imags(original, transformada, titulo1 = 'Antes', titulo2 = 'Después'):
    plt.subplot(1,2,1)
    plt.imshow(original)
    plt.title(titulo1)
    plt.subplot(1,2,2)
    plt.imshow(transformada)
    plt.title(titulo2)
    plt.show()

imagN = cv.imread('imag1.jpg') # CARGANDO IMAGEN NATURAL BGR
imagS = cv.imread('dibujo.png') # CARGANDO IMAGEN SINTÉTICA BGR

# Imagenes a RGB
RGB_imagN = cv.cvtColor(imagN, cv.COLOR_BGR2RGB) #BGR -> RGB
RGB_imagS = cv.cvtColor(imagS, cv.COLOR_BGR2RGB) #BGR -> RGB

plot_imags(imagN, RGB_imagN, 'BGR', 'RGB')
split_channs(RGB_imagN, 'Rojo', 'Verde', 'Azul')

plot_imags(imagS, RGB_imagS, 'BGR', 'RGB')
split_channs(RGB_imagS, 'Rojo', 'Verde', 'Azul')

#imagen a HSV
RGB_HSV(RGB_imagN)
RGB_HSV(RGB_imagS)

#imagen a L*a*b*
RGB_LAB(RGB_imagN)
RGB_LAB(RGB_imagS)