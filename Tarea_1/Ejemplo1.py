import numpy as np
import math
import matplotlib.pyplot as plt

# Señal de tiempo continuo
t=np.arange(0.0,1.0,0.001)
xt = 2*np.cos(2*np.pi*2*t) + 3*np.sin(2*np.pi*6*t)

# Discretización de la señal análoga
Ts=1.0/18.0
Fs=1.0/Ts
nT=np.arange(0.0,1.0,Ts)
xnT= 2*np.cos(2*np.pi*2*nT) + 3*np.sin(2*np.pi*6*nT)

plt.figure(1)
plt.plot(t, xt, color = 'red') 
plt.stem(nT,xnT) 
plt.title("Discretización") 
plt.xlabel("Tiempo(s)") 
plt.ylabel("Amplitud") 
plt.show()

# Señal de tiempo discreto
N=Fs
n=np.arange(0, N+1,1.0)
xn = 2*np.cos(2*np.pi*(2/Fs)*n) + 3*np.sin(2*np.pi*(6/Fs)*n)
plt.figure(2)
plt.stem(n, xn)
plt.title("Señal de tiempo discreto")
plt.xlabel("Muestras") 
plt.ylabel("Amplitud") 
plt.xticks(n,range(len(n)))
plt.show()