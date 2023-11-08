import serial
import numpy as np
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

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

def Update_data():
    global n
    global t

    while True:
        xt = 128 + amp * np.cos(2*np.pi*freq*t) #generando señal
        xt = round(xt, 2) # redondeo
        xtBytes = struct.pack('f', xt) # conversion a tipo bytes
        ser.write(xtBytes) # envia a puerto

        x_dat[n] = xt
        t_dat[n] = t
        t += Ts
        n += 1
        if n == 100:
            n = 0

freq = getSignalFrequency()
amp = getSignalAmplitude()

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

thread = threading.Thread(target = Update_data)

try:
    # open serial port
    ser = serial.Serial('/dev/pts/2',9600) #serial.Serial('/dev/ttys003', 9600)
    thread.start()
    ani = animation.FuncAnimation(fig, animate)
    plt.show()
    thread.join()
    ser.close()

except KeyboardInterrupt:
    print('Terminado por teclado')
    thread.join()
    plt.close()
    pass

