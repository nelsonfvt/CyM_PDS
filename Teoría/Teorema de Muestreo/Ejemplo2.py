import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# base de tiempo
Tf = 30
tsim = 0.01
t=np.arange(0, Tf, tsim)
# parámetros del sistema
m = 30
b = 20
k = 50

# Constantes de F. de transferencia
b1 = b/m
a1 = b1
b2 = k/m
a2 = b2
num = [b1, b2]
den = [1, b1, b2]

# Simulación: respuesta escalón
lti = signal.lti(num, den)
t, y = signal.step(lti, T = t)
plt.figure(1)
plt.plot(t, y)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Step response for 2. Order System')
plt.grid()

# Muestreo de la respuesta al escalón
Ns = 100 # submuestreo
pts = range(0,len(y),Ns)
nTs = t[pts]
yTs = y[pts]

plt.figure(2)
plt.plot(t, y)
plt.stem(nTs,yTs)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Step response for 2. Order System')
plt.grid()

# representación en tiempo discreto
N = len(nTs)
n = np.arange(0, N, 1.0)
plt.figure(3)
plt.stem(n,yTs)
plt.xlabel('Time [samples]')
plt.ylabel('Amplitude')
plt.title('Step response for 2. Order System')
plt.grid()
plt.show()