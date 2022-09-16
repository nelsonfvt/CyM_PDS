import cv2
import numpy as np
import matplotlib.pyplot as plt

imag1 = cv2.imread('imag1.jpg')

# tamaño de la imagen
print('Tamaño de la imagen: ', np.shape(imag1) )

#valor de un pixel
print('Un pixel (formato BGR): ', imag1[10][10]) #formato BGR

# Mostrar imagen metodo Opencv
cv2.imshow('imag1', imag1)
cv2.waitKey(0)
# presionar una tecla para cerrar la ventana

cv2.destroyAllWindows()

# Mostrar imagen método matplotlib
RGB_imag1 = cv2.cvtColor(imag1, cv2.COLOR_BGR2RGB) #correccion de formato
print('Un pixel (formato RGB): ', RGB_imag1[10][10])

plt.imshow(RGB_imag1)
plt.show()