import numpy as np
import matplotlib.pyplot as plt

# Señal de tiempo continuo
t=np.arange(0.0,1.0,0.001)
f1 = 4 #Hz
f2 = 6 #Hz
xt = 2*np.cos(2*np.pi*f1*t) + 3*np.sin(2*np.pi*f2*t)

# Discretización de la señal análoga
Fs=24.0
Ts=1.0/Fs
nT=np.arange(0.0,1.0,Ts)
xnT= 2*np.cos(2*np.pi*f1*nT) + 3*np.sin(2*np.pi*f2*nT)

plt.figure(1)
plt.plot(t, xt, color = 'red') 
plt.stem(nT,xnT) 
plt.title("Discretización de señal análoga") 
plt.xlabel("Tiempo (s)") 
plt.ylabel("Amplitud") 

# Señal de tiempo discreto
N=Fs
n=np.arange(0, N,1.0)
xn = 2*np.cos(2*np.pi*(f1/Fs)*n) + 3*np.sin(2*np.pi*(f2/Fs)*n)
plt.figure(2)
plt.stem(n, xn)
plt.title("Señal de tiempo discreto")
plt.xlabel("Muestras") 
plt.ylabel("Amplitud") 
plt.xticks(n,range(len(n)))
plt.show()