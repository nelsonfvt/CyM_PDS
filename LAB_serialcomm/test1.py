import serial
import numpy as np
import struct

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

# open serial port
ser = serial.Serial('/dev/ttys001', 9600)
t = 0
try:
    while True:
        xt = 128 + amp * np.cos(2*np.pi*freq*t)
        #tx = chr(int(val)).encode('utf-8')
        xt = round(xt, 2)
        #print(xt)
        xtBytes = struct.pack('f',xt)
        print(xtBytes)
        ser.write(xtBytes)
        t = t+0.01
except KeyboardInterrupt:
    pass

ser.close()

# t = np.arange(0.0,10.0,0.01)
# ser = serial.Serial('/dev/ttys001', 9600)
# for i in range(len(t)):
#     c = np.cos(2*np.pi*70*t[i])
#     val = 128 + 100 * c
#     tx = chr(int(val)).encode('utf-8')
#     ser.write(tx)
# ser.close()