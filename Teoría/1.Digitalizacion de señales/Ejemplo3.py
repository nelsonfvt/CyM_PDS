import numpy as np
import matplotlib.pyplot as plt

# Generación de señal análoga y gráfica
Ts = 1.0/24.0
t=np.arange(0.0,1.0,Ts/100.0)
f1 = 4 #Hz
f2 = 6 #Hz
xt = 2*np.cos(2*np.pi*f1*t) + 3*np.sin(2*np.pi*f2*t)
#Adicion ruido aleatorio
# c_noise = np.random.rand(len(t))
# xt = xt + 0.5*c_noise
plt.figure(1)
plt.plot(t, xt, color = 'blue') 
plt.title("Señal análoga") 
plt.xlabel("Tiempo (s)") 
plt.ylabel("Amplitud")
plt.grid()

# Discretización
samples = np.arange(0.0,1.0,Ts)
n = range(0,len(t),100)
nTs = t[n]
xnTs = xt[n]
plt.figure(2)
plt.plot(t, xt, color = 'red') 
plt.stem(nTs,xnTs) 
plt.title("Discretización de señal análoga") 
plt.xlabel("Tiempo (s)") 
plt.ylabel("Amplitud") 

# Cuantificación de la señal discretizada
ran = max(xt)-min(xt); #rango de la señal
nbits = 8 # numero bits de cuantificacion
nnivs = (np.power(2,nbits))-1 #numero de niveles de cuantificacion
delta = ran/nnivs #altura de nivel de cuantificacion
nive = np.arange(min(xt),max(xt),delta)
nivem = nive + (delta/2.0)
N = len(nTs)
xnq = np.zeros(N)
for i in range(0,N):
    j = 0
    while xnTs[i] > nivem[j]:
        j = j+1
    xnq[i] = nive[j]
# Gráfica
plt.figure(3)
plt.stem(nTs,xnq,linefmt='red',markerfmt='D') #senal cuantificada
plt.stem(nTs,xnTs,linefmt='grey') #señal discretizada sin cuantificar
plt.title("Señal discretizada y señal cuantificada") 
plt.xlabel("Tiempo (s)") 
plt.ylabel("Amplitud")

# Error de cuantificación
err = xnTs - xnq
plt.figure(4)
plt.stem(nTs,err) 
plt.title("Error de cuantificación") 
plt.xlabel("Tiempo (s)") 
plt.ylabel("Amplitud") 

plt.show()

# Medidas estadísticas
media_err = np.mean(err)
print('Media: ' + str(media_err))
desv_err = np.std(err)
print('Desv. Std.: ' + str(desv_err))