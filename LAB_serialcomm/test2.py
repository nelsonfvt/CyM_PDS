import numpy as np
import serial
import struct

# open serial port
ser = serial.Serial('/dev/ttys004', 9600)

try:
    while True:
        x = ser.read(4)
        xt = struct.unpack('f', x)
        print(xt[0])
except KeyboardInterrupt:
    pass

ser.close()