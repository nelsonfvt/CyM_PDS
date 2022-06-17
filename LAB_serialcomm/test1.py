import serial
import numpy as np

print('hello')

t = np.arange(0.0,10.0,0.01)
ser = serial.Serial('/dev/pts/6', 9600)
for i in range(len(t)):
    c = np.cos(2*np.pi*70*t[i])
    val = 128 + 100 * c
    tx = chr(int(val)).encode('utf-8')
    ser.write(tx)
ser.close()