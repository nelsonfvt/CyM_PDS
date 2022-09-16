import cv2
import numpy as np
import matplotlib.pyplot as plt


imagN = cv2.imread('imag1.jpg') # CARGANDO IMAGEN NATURAL
imagS = cv2.imread('dibujo.png', -1) # CARGANDO IMAGEN SINTÉTICA

# tamaño de la imagen
print('Tamaño de la imagen natural: ', np.shape(imagN) )
print('Tamaño de la imagen sintética: ', np.shape(imagS))

#valor de un pixel
print('Un pixel de la imágen natural (formato BGR): ', imagN[10][10]) #formato BGR
print('Un pixel de la imágen sintética (formato BGR): ', imagS[307][254]) #formato BGR

# Mostrar imagen metodo Opencv
cv2.imshow('IMAGEN NATURAL', imagN)
cv2.imshow('IMAGEN SINTETICA', imagS)

cv2.waitKey(0)
# presionar una tecla para cerrar la ventana y continuar

cv2.destroyAllWindows()

# Mostrar imagen método matplotlib
RGB_imagN = cv2.cvtColor(imagN, cv2.COLOR_BGR2RGB) #correccion de formato
RGB_imagS = cv2.cvtColor(imagS, cv2.COLOR_BGR2RGB) #correccion de formato
print('Un pixel (formato RGB): ', RGB_imagN[10][10])
print('Un pixel (formato RGB): ', RGB_imagS[307][254])

fig,axs = plt.subplots(2)

axs[0].imshow(RGB_imagN)
axs[1].imshow(RGB_imagS)

#plt.imshow(RGB_imagN)
plt.show()