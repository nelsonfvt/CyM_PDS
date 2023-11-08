import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
#from threading import Thread

def task():
    global n
    while True:
        x_vals[n] = n
        y_vals[n] = np.cos(2*np.pi*n/50)
        n += 1
        if n == 100:
            n = 0
    

fig = plt.figure(1)

# x = np.arange(0, 2*np.pi, 0.01)
# line, = ax.plot(x, np.sin(x))
x_vals = np.zeros(100)
y_vals = np.zeros(100)
n = 0

def animate(i):
    plt.cla()
    plt.plot(x_vals, y_vals)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')

t1 = threading.Thread(target = task)

try:
    t1.start()
    ani = animation.FuncAnimation(
    fig, animate, interval=200)
    plt.show()
except KeyboardInterrupt:
    print('Terminado por teclado')
    t1.join()
    plt.close()