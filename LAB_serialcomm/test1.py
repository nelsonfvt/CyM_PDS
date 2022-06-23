import serial
import numpy as np
import struct
import matplotlib.pyplot as plt

def getSignalFrequency():
    freq = -1.0
    while(freq < 1.0 or freq > 250.0):
        freq = float(input('Ingrese el valor de frecuancia en el rango [1.0 - 250.0]: '))
    return freq

def getSignalAmplitude():
    amp = -1.0
    while(amp < 10.0 or amp > 127.0):
        amp = float(input('Ingrese amplitud de la señal en el rango [10.0 - 127.0]: '))
    return amp


freq = getSignalFrequency()
amp = getSignalAmplitude()

try:
    # open serial port
    ser = serial.Serial('/dev/pts/2',9600) #serial.Serial('/dev/ttys003', 9600)
    
    # variables de tiempo
    t = 0
    Ts = 0.01 #Periodo de muestreo

    while True:
        xt = 128 + amp * np.cos(2*np.pi*freq*t) #generando señal
        #xt = chr(int(val)).encode('utf-8') #convierte a tipo char
        xt = round(xt, 2) # redondeo
        xtBytes = struct.pack('f', xt) # conversion a tipo bytes
        ser.write(xtBytes) # envia a puerto

        t = t + Ts
except KeyboardInterrupt:
    print('Terminado por teclado')
    pass

ser.close()