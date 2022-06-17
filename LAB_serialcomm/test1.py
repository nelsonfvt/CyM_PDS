import serial

print('hello')

ser = serial.Serial('/dev/pts/2', 9600)
print(ser.name)
for i in range(256):
    tx = chr(int(i)).encode('utf-8')
    ser.write(tx)
ser.close()