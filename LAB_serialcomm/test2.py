import numpy as np
import serial
import struct

# open serial port
ser = serial.Serial('/dev/ttys002', 9600)

try:
    while True:
        x = ser.read()
        xt = struct.unpack('b', x)
        print(xt)
except KeyboardInterrupt:
    pass

ser.close()