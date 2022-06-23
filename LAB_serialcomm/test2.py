import numpy as np
import serial
import struct

# open serial port
ser = serial.Serial('/dev/pts/3', 9600)
print(ser)

try:
    while True:
        x = ser.read(4)
        xt = struct.unpack('f', x)
        print(xt[0])
except KeyboardInterrupt:
    print('Terminado por teclado')
    pass

ser.close()