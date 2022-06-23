import serial
import numpy as np
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

def Read_data():
    global n
    global t
    
    while True:
        x = ser.read(4)
        xt = struct.unpack('f', x)
        #print(xt[0])
        t_dat[n] = t
        x_dat[n] = xt[0]

        t += Ts
        n += 1
        if n == 100:
            n = 0
    

fig = plt.figure(1)
t_dat = np.zeros(100)
x_dat = np.zeros(100)

# variables de tiempo
t = 0
Ts = 0.01 #Periodo de muestreo (segundos)
n = 0

def animate(i):
    plt.cla()
    plt.plot(t_dat,x_dat, color = 'red')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

thread = threading.Thread(target = Read_data)

try:
    ser = serial.Serial('/dev/pts/3', 9600)
    thread.start()
    ani = animation.FuncAnimation(fig, animate)
    plt.show()
    ser.close()

except KeyboardInterrupt:
    print('Terminado por teclado')
    thread.join()
    ser.close()
    plt.close()
    pass