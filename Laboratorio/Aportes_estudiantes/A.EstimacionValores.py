
'''

EXTEND KALMAN FILTER (EKF) - FILTRO EXTENDIDO KALMAN
Universidad Militar Nueva Granada
Ingenieria Mecatronica 7 Semestre

Codigo Elaborado por:
Version V6
- Leyder Leoncio Rodriguez Rodriguez
- David Alejandro Duarte Montañez
- Melanie Gabriela Polo Gomez
- Angel Santiago Marquez
- Julian Andres Prieto
- Jairo Valero
- David Espejo
- Leyva angulo
- Jorge Caceres
- Daniela Urrego
'''

# LIBRERIAS USADAS
import sys
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import serial
import threading
import itertools
import csv
from LectorCsv import *
from LeerTiempoReal import *

# Variables y librerias para copelia
import sim

# LIBRERIAS PROPRIAS

contadorCsv=0
#/////////////////Copelia Librerias///////////////
def connect(port):
    sim.simxFinish(-1)
    clientID= sim.simxStart('127.0.0.1', port, True, True, 1000,5)
    if clientID ==0 : print("conectado a ", port )
    else: print("no se pudo conectar ")
    return clientID
 #Cinematica inversa

def Inv_model(EF):
    a = np.array([0.0, 0.25, 0.30])
    d = np.array([0.22, 0.0, 0.0])
    T = np.array([0.0, 0.0, 0.0])

    EF[2] = EF[2] - d[0]

    T[0] = np.arctan2(EF[1], EF[0])

    c3 = ( EF[0]**2 + EF[1]**2 + EF[2]**2 -a[1]**2 -a[2]**2 ) / (2 * a[1] * a[2])
    #print(c3)
    s3 = math.sqrt(1 - c3**2)
    T[2] = np.arctan2(s3, c3)

    s2 = ( (a[1]+a[2]*c3)*EF[2] - a[2]*s3*math.sqrt(EF[0]**2 + EF[1]**2) ) / (EF[0]**2 + EF[1]**2 + EF[2]**2)
    c2 = ( (a[1]+a[2]*c3)*math.sqrt(EF[0]**2 + EF[1]**2 + a[2]*s3*EF[2]) ) / (EF[0]**2 + EF[1]**2 + EF[2]**2)
    T[1] = np.arctan2(s2, c2)
    
    #print("Resultado M.I: ")
    #print(T)
    #print('\n')
    return T


cantidaddatos = 100000
#variables copelia
contadorenvio=1
clientID= connect(19999) #conexion a copelia
x = np.full(cantidaddatos, 0.000000)



# VARIABLES A INGRESAR
theta1 = 10.0*(np.pi/180.0)
theta1_p = 0.000
theta1_p_p = 0.000

theta2 = 5.0*(np.pi/180.0)
theta2_p = 0.000
theta2_p_p = 0.000

m1=5.0
m2=5.0

l1=25/100.0
l2=32/100.0

distancia = 0.0

X1 = 0.0
Y2 = 0.0


# TIEMPO DE MUESTREO
f = 100
Ts = 1/f
T=Ts

#redondeo
Vredon = 6

#grafocas
GrapicaX=np.full(cantidaddatos, 0.000000)
GrapicaY=np.full(cantidaddatos, 0.000000)
Grapicatheta1=np.full(cantidaddatos, 0.000000)
Grapicatheta2=np.full(cantidaddatos, 0.000000)

# MATRICES DEL FILTRO KALMAN 6x6
# Pk INICIAL 6x6
PK =np.array( [ [1.0, 0, 0, 0, 0, 0],
                 [0, 1.0, 0, 0, 0, 0],
                 [0, 0, 1.0, 0, 0, 0],
                 [0, 0, 0, 1.0, 0, 0],
                 [0, 0, 0, 0, 1.0, 0],
                 [0, 0, 0, 0, 0, 1.0]]) 


# Qk INICIAL 6x6

# Q PRIMERA ITERACION
'''


                
                
# VALORES CORRECTOS PRIMERA VEZ
QK =np.array( [[ 1.32620469e+02,  6.77432500e+00, -5.19700000e-02, -0.00000000e+00, 3.71946500e+00, -4.44922000e-01],
            [ 6.77432500e+00,  1.32621021e+02,  5.19690000e-02,  0.00000000e+00, -3.71948100e+00,  4.44925000e-01],
            [-0.05197,   0.051969,  0.05158,  -0.,       -0.007951,  0.011705],
            [-0.,  0., -0.,  0., -0.,  0.],
            [ 3.719465, -3.719481, -0.007951, -0.,        0.225201, -0.02847 ],
            [-0.444922,  0.444925,  0.011705,  0.,       -0.02847,   0.018885]])


'''

# Qk INICIAL 6x6
QK =np.array( [[ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,],
            [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,],
            [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,],
            [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,],
            [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,],
            [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,]])

# Yk INICIAL 6x6
Yk = np.array( [ [0.0],
                [0.0],
                [0.0]])


# LECTURA DATOS TOMADOS ANTERIORMENTE Por CSV
#valiu = LeerArchivoCsv()
#Ax=valiu[:,0]
#Ay=valiu[:,1]
#Gz=valiu[:,2]


# LECTURA DE DATOS POR COM
Datos = ConexionToCom()


# COMPENSACION (VECTORES )
for n in range(1000):
    
    Aux = Datos.LeerDatoActual()
    # print(Aux)
    Datos.AgregarLista(Aux[0],Aux[1],Aux[2])


# PROMEDIO DE LOS DATOS
Prom = Datos.QuitarNivelDC()
covarianza = Datos.CovarianzaSensores(Prom)

print("Nivel Dc calculado:")
print(Prom)
print("...")

# Rk INICIAL 3x3

RK = np.array( [[ covarianza[0], 0, 0],
                [0, covarianza[1],0],
                [0, 0, covarianza[2]]])

'''
print("Matriz Rk Actualizada")
for Rkescrita in RK:
    print(np.round(Rkescrita, 6))
'''

# ===== Inicio cilclo for =====

# use of range() to define a range of values
values = range(cantidaddatos)

# iterate from i = 0 to i = 3
theta1_p_p = ((-2*(math.sin(theta1-theta2)))*m2*((pow(theta2_p,2)*l2) + (pow(theta1_p,2)*l1)*(math.cos(theta1-theta2)))) / (l1*((2*m1) + m2 - (m2*math.cos((2*theta1) - (2*theta2)))))
theta2_p_p = (2*(math.sin(theta1-theta2))*(pow(theta1_p,2)*l1*(m1+m2) + (pow(theta2_p,2)*l2*m2)*math.cos(theta1-theta2))) / (l2*((2*m1) + m2 - (m2*math.cos((2*theta1) - (2*theta2))))) 

# MATRIZ ESTIMADA DE X
Xk = np.array([ [theta1],
                [theta2],
                [theta1_p],
                [theta2_p],
                [theta1_p_p],
                [theta2_p_p]])
try:
    try:

        # ==== CICLO INFINITO ====

        for i in values:

            # ECUACIONES DERIVADA RESPECTO A THETA 1 PP (ACELERACION DEL SISTEMA)
            theta1_pp_T1 = (2*pow(theta1_p,2)*m2*pow(math.sin(theta1 - theta2),2))/(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)) - (2*m2*math.cos(theta1 - theta2)*(l1*math.cos(theta1 - theta2)*pow(theta1_p,2) + pow(theta2_p,2))) / (l1*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))) + (4*pow(m2,2)*math.sin(theta1 - theta2)*math.sin(2*theta1 - 2*theta2)*(l1*math.cos(theta1 - theta2)*pow(theta1_p,2) +pow(theta2_p,2)))/(l1*pow(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2),2))
            theta1_pp_T2 = (2*m2*math.cos(theta1 - theta2)*(l1*math.cos(theta1 - theta2)*pow(theta1_p,2) + pow(theta2_p,2)))/(l1*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))) - (2*pow(theta1_p,2)*m2*pow(math.sin(theta1 - theta2),2))/(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)) - (4*pow(m2,2)*math.sin(theta1 - theta2)*math.sin(2*theta1 - 2*theta2)*(l1*math.cos(theta1 - theta2)*pow(theta1_p,2) + pow(theta2_p,2)))/(l1*pow(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2),2))
            theta1_pp_dT1 = (-4 * theta1_p * m2 * math.cos(theta1-theta2) * math.sin(theta1-theta2)) / (2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))
            theta1_pp_dT2 = (-4 *theta2_p * m2 * math.sin(theta1-theta2)) / (l1*(2*m1 + m2 - m2*math.cos(2*theta1-2*theta2)))

            # ECUACIONES DERIVADA RESPECTO A THETA 2 PP (ACELERACION DEL SISTEMA)
            theta2_pp_T1 = (2*math.cos(theta1 - theta2)*(l1*(m1 + m2)*pow(theta1_p,2) + l2*m2*math.cos(theta1 - theta2)*pow(theta2_p,2)))/(l2*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))) - (2*pow(theta2_p,2)*m2*pow(math.sin(theta1 - theta2),2))/(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)) - (4*m2*math.sin(theta1 - theta2)*math.sin(2*theta1 - 2*theta2)*(l1*(m1 + m2)*pow(theta1_p,2) + l2*m2*math.cos(theta1 - theta2)*pow(theta2_p,2)))/(l2*pow((2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)),2))
            theta2_pp_T2 = (2*pow(theta2_p,2)*m2*pow(math.sin(theta1 - theta2),2)) / (2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)) - (2*math.cos(theta1 - theta2)*(l1*(m1 + m2)*pow(theta1_p,2) + l2*m2*math.cos(theta1 - theta2)*pow(theta2_p,2)))/(l2*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))) + (4*m2*math.sin(theta1 - theta2)*math.sin(2*theta1 - 2*theta2)*(l1*(m1 + m2)*pow(theta1_p,2) + l2*m2*math.cos(theta1 - theta2)*pow(theta2_p,2)))/(l2*pow(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2),2))
            theta2_pp_dT1 = (4*theta1_p*l1*math.sin(theta1 - theta2)*(m1 + m2)) / (l2*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)))
            theta2_pp_dT2 = (4*theta2_p*m2*math.cos(theta1 - theta2)*math.sin(theta1 - theta2)) / (2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2))

            # ---- MATRIZ F
            FK = np.array([ [1.0, 0, Ts, 0, 0, 0],
                            [0, 1.0, 0, Ts, 0, 0],
                            [0, 0, 1.0, 0, (pow(Ts,2)/2), 0],
                            [0, 0, 0, 1.0, 0, (pow(Ts,2)/2)],
                            [theta1_pp_T1, theta1_pp_T2, theta1_pp_dT1, theta1_pp_dT2, 1.0, 0],
                            [theta2_pp_T1, theta2_pp_T2, theta2_pp_dT1, theta2_pp_dT2, 0, 1.0]])

            #print("Matriz Linealizada FK")
            #for PfLinealizada in FK:
                #print(np.round(PfLinealizada, 6))
            #print("")
            # MATRIZ ESTIMADA DE X
            Xk = np.array([ [theta1],
                            [theta2],
                            [theta1_p],
                            [theta2_p],
                            [theta1_p_p],
                            [theta2_p_p]])
            # MATRIZ TRANSPUESTA FK
            FKtranspuesta = np.transpose(FK)

            # CALCULO ACELERACION (T_pp T_p T)
            theta1_p_p = ((-2*(math.sin(theta1-theta2)))*m2*((pow(theta2_p,2)*l2) + (pow(theta1_p,2)*l1)*(math.cos(theta1-theta2)))) / (l1*((2*m1) + m2 - (m2*math.cos((2*theta1) - (2*theta2)))))
            theta2_p_p = (2*(math.sin(theta1-theta2))*(pow(theta1_p,2)*l1*(m1+m2) + (pow(theta2_p,2)*l2*m2)*math.cos(theta1-theta2))) / (l2*((2*m1) + m2 - (m2*math.cos((2*theta1) - (2*theta2)))))
             
            # Calculo de theta 1 y theta 2 punto
            theta1_p = (theta1_p_p*T) + theta1_p
            theta2_p = (theta2_p_p*T) + theta2_p
            
            # Calculo de theta 1 y theta 2 Actualizados
            theta1=((theta1_p_p*(pow(T,2)/2)+(theta1_p))*T) + theta1
            theta2=((theta2_p_p*(pow(T,2)/2)+(theta2_p))*T) + theta2



            # ===== INCIO FILTRO KALMAN =====

            # ----- PRIMER PASO STATE ESTIMATE -----
            #print("1. Prediccion de los estados xk = f(xk,uk)")

            # FORMULAS DEL MODELO

           

            #print("")


            # ----- SEGUNDO PASO COVARIANCE ESTIMATE -----
            #print("2. Prediccion de covarianza estimada")

            # ESPACIOS DE ESTADOS T1 T2 dT1 dT2 ddT1 ddT2 

            

            # FORMULA PK = Fk * Pk Ft + Qk
            PK = FK*PK*FKtranspuesta + QK

            #print("Matriz PK Resultante")
            #for Pkescrita in PK:
                #print(np.round(Pkescrita, 6))
                
            #print("")


            # ----- TERCER PASO RESIDUAL ESTIMATE -----
            #print("3. Medision residual")
            
            #Habilitar si es con csv
            #Zk = np.array([ [Ax[i]],   #sensor     x
            #                [Ay[i]],   #sensor     y
            #                [Gz[i]]])  #sen giro   z
            
            #habilitar si es con tiempo real
            #print("Datos sensor (sin media): ")
            Aux = Datos.LeerDatoActual()
            print(Aux[0]-Prom[0])

            Zk = np.array([ [Aux[0]-Prom[0]],   #sensor     x
                            [Aux[1]-Prom[1]],   #sensor     y
                            [Aux[2]-Prom[2]]])  #sen giro   z
            
            # ECUACIONES DEL MODELO DEL SENSOR
            X_p_p = -l1 * (theta1_p_p * math.sin(theta1) + pow(theta1_p,2) * math.cos(theta1)) - l2*(theta2_p_p*math.sin(theta2) + pow(theta2_p,2) * math.cos(theta2))
            Y_p_p = l1 * (theta1_p_p * math.cos(theta1) - pow(theta1_p,2) * math.sin(theta1)) + l2*(theta2_p_p*math.cos(theta2) - pow(theta2_p,2) * math.sin(theta2))

            # TRANSFORMADA DEL MODELO LINEAL
            Sx_p_p = math.cos(theta2+(math.pi/2))*X_p_p + math.sin(theta2+(math.pi/2))*Y_p_p
            Sy_p_p = -math.sin(theta2+(math.pi/2))*X_p_p + math.cos(theta2+(math.pi/2))*Y_p_p
            Wz = theta2_p

            # MATRIZ hx
            hxK = np.array([ [Sx_p_p],   #sensor     x
                            [Sy_p_p],   #sensor     y
                            [Wz]])  #sen giro   z

            # FORMULA MEDICION RESIDUAL
            Yk = Zk - hxK

            #print("Matriz YK Resultante")
            #for YkEscrita in Yk:
                #print(np.round(YkEscrita, 6))    
            #print("")


            # ----- CUARTO PASO COVARIANCE -----
            #print("4. Actualizacion Covarianza")

            # ---- MATRIZ DEL SENSOR 3X6  (H)

            # ECUACIONES DERIVADA RESPECTO A Sx 1 PP (ACELERACION DEL SENSOR)
            Sx_pp_T1 = l1*math.cos(theta2 + math.pi/2)*(pow(theta1_p,2)*math.sin(theta1) - theta1_p_p*math.cos(theta1)) - l1*math.sin(theta2 + math.pi/2)*(math.cos(theta1)*pow(theta1_p,2) + theta1_p_p*math.sin(theta1))
            Sx_pp_T2 = math.sin(theta2 + math.pi/2)*(l1*(math.cos(theta1)*pow(theta1_p,2) + theta1_p_p*math.sin(theta1)) + l2*(math.cos(theta2)*pow(theta2_p,2) + theta2_p_p*math.sin(theta2))) - math.cos(theta2 + math.pi/2)*(l1*(pow(theta1_p,2)*math.sin(theta1) - theta1_p_p*math.cos(theta1)) + l2*(pow(theta2_p,2)*math.sin(theta2) - theta2_p_p*math.cos(theta2))) + l2*math.cos(theta2 + math.pi/2)*(pow(theta2_p,2)*math.sin(theta2) - theta2_p_p*math.cos(theta2)) - l2*math.sin(theta2 + math.pi/2)*(math.cos(theta2)*pow(theta2_p,2) + theta2_p_p*math.sin(theta2))
            Sx_pp_dT1 = -2*l1*theta1_p*math.sin(theta1)*math.sin(theta2 + math.pi/2) - 2*l1*theta1_p*math.cos(theta1)*math.cos(theta2 + math.pi/2)
            Sx_pp_dT2 = -2*l2*theta2_p*math.sin(theta2)*math.sin(theta2 + math.pi/2) - (2*l2*theta2_p*math.cos(theta2)*math.cos(theta2 + math.pi/2))
            Sx_pp_ddT1 = l1*math.cos(theta1)*math.sin(theta2 + math.pi/2) - l1*math.cos(theta2 + math.pi/2)*math.sin(theta1)
            Sx_pp_ddT2 = l2*math.cos(theta2)*math.sin(theta2 + math.pi/2) - l2*math.cos(theta2 + math.pi/2)*math.sin(theta2)

            # ECUACIONES DERIVADA RESPECTO A Sy 2 PP (ACELERACION DEL SENSOR)
            Sy_pp_T1 = - l1*math.cos(theta2 + (math.pi/2))*(math.cos(theta1)*pow(theta1_p,2) + theta1_p_p*math.sin(theta1)) - l1*math.sin(theta2 + math.pi/2)*(pow(theta1_p,2)*math.sin(theta1) - theta1_p_p*math.cos(theta1))
            Sy_pp_T2 = math.cos(theta2 + (math.pi/2))*(l1*(math.cos(theta1)*pow(theta1_p,2) + theta1_p_p*math.sin(theta1)) + l2*(math.cos(theta2)*pow(theta2_p,2) + theta2_p_p*math.sin(theta2))) + math.sin(theta2 + (math.pi/2))*(l1*(pow(theta1_p,2)*math.sin(theta1) - theta1_p_p*math.cos(theta1)) + l2*(pow(theta2_p,2)*math.sin(theta2) - theta2_p_p*math.cos(theta2))) - l2*math.cos(theta2 + math.pi/2)*(math.cos(theta2)*pow(theta2_p,2) + theta2_p_p*math.sin(theta2)) - l2*math.sin(theta2 + math.pi/2)*(pow(theta2_p,2)*math.sin(theta2) - theta2_p_p*math.cos(theta2))
            Sy_pp_dT1 = 2*l1*theta1_p*math.cos(theta1)*math.sin(theta2 + (math.pi/2)) - 2*l1*theta1_p*math.cos(theta2 + (math.pi/2))*math.sin(theta1)
            Sy_pp_dT2 = 2*l2*theta2_p*math.cos(theta2)*math.sin(theta2 + (math.pi/2)) - 2*l2*theta2_p*math.cos(theta2 + (math.pi/2))*math.sin(theta2)
            Sy_pp_ddT1 = l1*math.cos(theta1)*math.cos(theta2 + math.pi/2) + l1*math.sin(theta1)*math.sin(theta2 + math.pi/2)
            Sy_pp_ddT2 = l2*math.cos(theta2)*math.cos(theta2 + math.pi/2) + (l2*math.sin(theta2)*math.sin(theta2 + math.pi/2))

            # ---- MATRIZ H
            HK = np.array([ [Sx_pp_T1, Sx_pp_T2, Sx_pp_dT1, Sx_pp_dT1, Sx_pp_ddT1, Sx_pp_ddT2],
                            [Sy_pp_T1, Sy_pp_T2, Sy_pp_dT1, Sy_pp_dT1, Sy_pp_ddT1, Sy_pp_ddT2],
                            [0, 0, 0, 1.0, 0, 0]])

            #print("Matriz H Lineal")
            #for jacobiando_HK in HK:
                #print(np.round(jacobiando_HK,6))
            #print("")

            # MATRIZ TRANSPUESTA HK
            HKtranspuesta = np.transpose(HK)

            # FORMULA SK = Hk * Pk * Hk(T) + Rk             // MULTIPLICAR MATRICES DE DISTINTAS FILAS Y COLUMNAS @ o np.dot(A,B)
            #SK = HK @ PK @ HKtranspuesta + RK
            SK = np.dot(HK, np.dot(PK,HKtranspuesta)) + RK

            #print("Matriz SK Resultante")
            #for Skescrita in SK:
                #print(np.round(Skescrita, 6))
                
            #print("")


            # ----- QUINTO PASO GANANCIA KALMAN -----
            #print("5. Ganancia Kalman")

            # INVERSO DE LA MATRIZ SK
            SK_inv = np.linalg.inv(SK)

            # FORMULA K K_ganancia = Pk  HKtranspuesta * SK_inv
            K_ganancia = np.dot(PK, np.dot(HKtranspuesta,SK_inv))

            #print("Matriz Kganancia Resultante")
            #for Kganescrita in SK:
                #print(np.round(Kganescrita, 6))
                
            #print("")


            # ----- SEXTO ACTUALIZACION DE LAS VARIABLES -----
            #print("6. Matriz Xk actualizada")
            Xk = Xk + K_ganancia @ Yk
            theta1=float(Xk[0])
            theta2=float(Xk[1])
            theta1_p=float(Xk[2])
            theta2_p=float(Xk[3])
            theta1_p_p=float(Xk[4])
            theta2_p_p=float(Xk[5])
            
            print("6. Matriz xk Actualizada")
            for xKactualziadaescrita in Xk:
                print(np.round(xKactualziadaescrita, 6)) 
            print("")


            # ECUACIONES DEL MODELO SENSOR FINAL
            X1 = l1*math.cos(theta1) + l2*math.cos(theta2)
            Y2 = l1*math.sin(theta1) + l2*math.sin(theta2)
            z = 0.22 ## 0.22 

            # GRAFICA FINAL
            #actualizar_grafica(Xk[0], Xk[1])
            Grapicatheta1[i]= (float(Xk[0]))
            Grapicatheta2[i]= (float(Xk[1]))
            GrapicaX[i]= (float(X1))
            GrapicaY[i]= (float(Y2))
            x[i]= (i)
            contadorCsv=i

            if contadorenvio==0:
                ##Obtener manejador de las articulaciones
                ret,joint0=sim.simxGetObjectHandle(clientID, 'joint0', sim.simx_opmode_blocking)
                ret,joint1=sim.simxGetObjectHandle(clientID, 'joint1', sim.simx_opmode_blocking)
                ret,joint2=sim.simxGetObjectHandle(clientID, 'joint2', sim.simx_opmode_blocking)
                ##print(joint2)

                # MODELO INVERSO
                EF = np.array([X1, Y2, z])

                for k in range(1, len(sys.argv)):
                    EF[k-1] = float(sys.argv[k])

                #print(Inv_model(EF))
                radianes= Inv_model(EF)
                # ##radianes[0]=radianes[0]+(np.pi/2)
                radianes[1]=radianes[1]-(np.pi/2)
                # ##radianes[2]=radianes[2]+(np.pi/2)

                returnCode = sim.simxSetJointTargetPosition(clientID, joint0,radianes[0], sim.simx_opmode_oneshot)
                print(returnCode)
                returnCode2 = sim.simxSetJointTargetPosition(clientID, joint1,radianes[1], sim.simx_opmode_oneshot)
                print(returnCode2)
                returnCode3 = sim.simxSetJointTargetPosition(clientID, joint2,radianes[2], sim.simx_opmode_oneshot)
                print(returnCode3)

                ##Obtener posicion brazo 
                ##print("Posicion del brazo en coppelia")
                ##returnCode, pos0 = sim.simxGetJointPosition(clientID, joint0, sim.simx_opmode_blocking)
                ##print(pos0)
                ##returnCode, pos1 = sim.simxGetJointPosition(clientID, joint1, sim.simx_opmode_blocking)
                ##print(pos1)
                ##returnCode, pos2 = sim.simxGetJointPosition(clientID, joint2, sim.simx_opmode_blocking)
                ##print(pos2)

                
                ##Obtener manejador del Dummy

                returnCode,handle = sim.simxGetObjectHandle(clientID, 'Dummy', sim.simx_opmode_blocking)
                dummy = handle
                ##print(dummy)
                print("posicion del Dummy")
                retCode,pos = sim.simxGetObjectPosition(clientID, dummy, -1, sim.simx_opmode_blocking)
                #pos[2]=pos[2]-0.22295 ## suma del desface del sistema de referencias del robot en coppelia frente al codigo
                print(pos)
                contadorenvio=0
            
            contadorenvio=contadorenvio+1
            


            # GRAFICA A TIEMPO REAL
            '''
            x_data.append(i)
            y1_data.append(Xk[0])
            y2_data.append(Xk[1])
            '''

            # ----- SEPTIMA ACTUALIZACION DE P -----
            Identidad = np.array(   [   [1.0, 0, 0, 0, 0, 0],
                                        [0, 1.0, 0, 0, 0, 0],
                                        [0, 0, 1.0, 0, 0, 0],
                                        [0, 0, 0, 1.0, 0, 0],
                                        [0, 0, 0, 0, 1.0, 0],
                                        [0, 0, 0, 0, 0, 1.0]]) 

            PK = (Identidad - K_ganancia @ HK) @ PK


            print("7. Matriz Pk actualizada: ")
            for PkActualizadaescrita in PK:
                print(np.round(PkActualizadaescrita, 6))
            print('\n')

            
            isNaN_X = np.isnan(PK)
            #isNaN_Y = np.isnan(theta2)

            if(isNaN_X[0][0] == True):
                print("Error S  lir")


    except :
        
        print("error en lectura")    
        print(contadorenvio)
        pass

except KeyboardInterrupt:
        
    # Salir del bucle si se presiona Ctrl+C   
    pass
#input("enter para salir")


# IMPRESION DE LA GRAFICA
name=(str(contadorCsv)+"Output.csv")
newfile = np.savetxt(name, np.dstack((GrapicaX,GrapicaY))[0],"%f,%f",header="x,y")
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(x,Grapicatheta1)
axs[0, 0].set_title('Thetha 1')
axs[0, 1].plot(x,Grapicatheta2, 'tab:orange')
axs[0, 1].set_title('Thetha 2')
axs[1, 0].plot(x, GrapicaX, 'tab:green')
axs[1, 0].set_title('X')
axs[1, 1].plot(x, GrapicaY, 'tab:red')
axs[1, 1].set_title('Y')
  

plt.show()


            


