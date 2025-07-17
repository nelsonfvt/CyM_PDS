import numpy as np
import matplotlib.pyplot as plt

# Dimensiones del robot en metros
l=0.2 # distancia centro del robot - rueda
r=0.05 # radio de la rueda
ri=0.05 # distancia centro del robot - IMU

# Periodo de muestreo
ts = 1.0/100.0 #segundos

# Velocidades angulares de las ruedas
wr = np.pi #derecha - rad/seg
wl = 0.5 * np.pi #izquierda - rad/seg

# Postura inicial del robot
theta = np.pi / 3.0 #orientacion - radianes
X = 0.0 #posicion - metros
Y = 0.0
# Velocidades iniciales del robot
x_punto = 0.0 
y_punto = 0.0
theta_punto = 0.0

X_vec = np.zeros(1000)
Y_vec = np.zeros(1000)

# Matriz Q

Q = np.array([[2.500000000000000e-09, 5.000000000000001e-07, 0, 0, 0, 0],
            [5.000000000000001e-07, 1.000000000000000e-04, 0, 0, 0, 0],
            [0, 0, 2.500000000000000e-09, 5.000000000000001e-07, 0, 0],
            [0, 0, 5.000000000000001e-07, 1.000000000000000e-04, 0, 0],
            [0, 0, 0, 0, 2.500000000000000e-09, 5.000000000000001e-07],
            [0, 0, 0, 0, 5.000000000000001e-07, 1.000000000000000e-04]])

# Matriz R
R = np.eye(5) * 0.1

# Matriz P
P = np.eye(6)*0.1

#Vector de estados
estados = np.array([X,
                    x_punto,
                    Y,
                    y_punto,
                    theta,
                    theta_punto])

# Simulacion 10 segundos

for i in range(0,1000):
    #atrasos de los estados
    x_p_n1 = estados[1]
    y_p_n1 = estados[3]
    theta_p_n1 = estados[5]

    # PREDICT
    # Calculo de velocidades del chasis
    V = r/2 * (wr + wl) # velocidad lineal
    estados[5] = r/(2*l) * (wr - wl) # velocidad angular

    # Calculo de velocidades dese el sist refe global
    estados[1] = V * np.cos(estados[4])
    estados[3] = V * np.sin(estados[4])

    # Calculo orientacion del robot
    estados[4] = estados[5]*ts + estados[4]
    # Caluclo posicion del robot
    estados[0] = estados[1]*ts + estados[0]
    estados[2] = estados[3]*ts + estados[2]

    # Matriz F - Jacobiano
    
    F = np.array([[1, ts, 0, 0, 0, 0],
                [0, 0, 0, 0, np.sin(estados[4])*(r/2)*(wr+wl), 0],
                [0, 0, 1, ts, 0, 0],
                [0, 0, 0, 0, np.cos(estados[4])*(r/2)*(wr+wl), 0],
                [0, 0, 0, 0, 1, ts],
                [0, 0, 0, 0, 0, 1]])

    # Actualización Matriz P
    P = F.dot(P.dot(F.transpose())) + Q

    # UPDATE
    # Calculo hx
    A_x = (estados[1] - x_p_n1) / ts
    A_y = ri * (estados[5] - theta_p_n1) / ts
    E_l = (np.sqrt(estados[1]**2 + estados[3]**2) - estados[5]*l) / r
    E_r = (np.sqrt(estados[1]**2 + estados[3]**2) + estados[5]*l) / r
    W_z = estados[5]

    hx = np.array([A_x,
                A_y,
                E_l,
                E_r,
                W_z])

    #Comparacion con sensores - calculo y_m
    #Capturar sensores
    z = np.zeros(5)
    y_m = z - hx

    # Matriz H - Jacobiano
    H = np.array([[0, 1.0/ts, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, ri/ts],
                 [0, estados[1]/(np.sqrt(estados[1]**2 + estados[3]**2)*r), 0, -estados[3]/(np.sqrt(estados[1]**2 + estados[3]**2)*r), 0, l/r],
                 [0, estados[1]/(np.sqrt(estados[1]**2 + estados[3]**2)*r), 0, -estados[3]/(np.sqrt(estados[1]**2 + estados[3]**2)*r), 0, -l/r],
                 [0, 0, 0, 0, 0, 1]])

    # Calculo de ganancia de Kalman
    S = H.dot(P.dot(H.transpose())) + R
    K = P.dot(H.transpose()).dot(np.linalg.inv(S))

    # Ajuste de estados
    estados = estados + K.dot(y_m)

    # Ajsute Matriz P
    P = (np.eye(6) - K.dot(H)).dot(P)

    # Almacena datos
    X_vec[i] = estados[0]
    Y_vec[i] = estados[2]

# Visualizacion de trayectoria
plt.figure(1)
plt.scatter(X_vec, Y_vec)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.grid(1)
plt.show()