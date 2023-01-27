import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def rotate_imag(img, ang):
    rows,cols = img.shape

    M = cv.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), ang, 1)
    dst = cv.warpAffine(img, M, (cols,rows))

    plot_imags(img,dst)

def trans_imag(img, x ,y):
    rows,cols = img.shape
    M = np.float32([[1,0,x],[0,1,y]])
    dst = cv.warpAffine(img,M,(cols,rows))
    
    plot_imags(img,dst)
    
def affine_imag(img):
    rows,cols = img.shape

    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,200]])

    M = cv.getAffineTransform(pts1,pts2)
    dst = cv.warpAffine(img,M,(cols,rows))
    plot_imags(img,dst)

def plot_imags(img,dst):
    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')

    plt.subplot(1,2,2)
    plt.imshow(dst,'gray')
    plt.title('Transformada')
    plt.show()

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

# Translación
trans_imag(imagN, 100, 50)
trans_imag(imagS, 150, -100)

# Rotación
rotate_imag(imagN,90)
rotate_imag(imagS,-45)

# Affine
affine_imag(imagN)
affine_imag(imagS)