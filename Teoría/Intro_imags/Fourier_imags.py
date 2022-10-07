import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def F_spectrum(img):
    dft = cv.dft(np.float32(img), flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    mag_spec = 20 * np.log(cv.magnitude(dft[:,:,0], dft[:,:,1]))
    mag_spec_shift = 20 * np.log(cv.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))

    plt.subplot(1,3,1)
    plt.imshow(img, 'gray')
    plt.title('Original')
    plt.subplot(1,3,2)
    plt.imshow(mag_spec, 'gray')
    plt.title('Mag espectro')
    plt.subplot(1,3,3)
    plt.imshow(mag_spec_shift, 'gray')
    plt.title('Mag espectro shift')
    plt.show()

def F_HighPF(img):
    rows, cols = img.shape
    crow,ccol = rows//2 , cols//2
    dft = cv.dft(np.float32(img), flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    mask = np.ones((rows,cols,2),np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 0
    
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv.idft(f_ishift)
    img_back = cv.magnitude(img_back[:,:,0], img_back[:,:,1])

    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(img_back,'gray')
    plt.title('Filtrada')
    plt.show()

def F_LowPF(img):
    rows, cols = img.shape
    crow,ccol = rows//2 , cols//2
    dft = cv.dft(np.float32(img), flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    mask = np.zeros((rows,cols,2),np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1
    
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv.idft(f_ishift)
    img_back = cv.magnitude(img_back[:,:,0], img_back[:,:,1])

    plt.subplot(1,2,1)
    plt.imshow(img,'gray')
    plt.title('Original')
    plt.subplot(1,2,2)
    plt.imshow(img_back,'gray')
    plt.title('Filtrada')
    plt.show()

imagN = cv.imread('imag1.jpg', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN NATURAL
imagS = cv.imread('dibujo.png', cv.IMREAD_GRAYSCALE) # CARGANDO IMAGEN SINTÉTICA

F_spectrum(imagN)
F_spectrum(imagS)

F_HighPF(imagN)
F_HighPF(imagS)

F_LowPF(imagN)
F_LowPF(imagS)