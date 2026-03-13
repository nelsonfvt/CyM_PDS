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
# LIBRERIAS TIEMPO REAL
import os
import serial
#import pandas as pd
import numpy as np
import statistics
from itertools import repeat
import time
import math
class ConexionToCom:
    
    # VARIABLES Y LECTURA
    def __init__(self):
        
        # LECTURA SERIAL
        self.datosSerial = serial.Serial('COM4', 1000000)

        # VECTOR LECTURA
        self.Vector=[0.0,0.0,0.0]

        # COMPENSACION
        self.ToCompensAx=[]
        self.ToCompensAy=[]
        self.ToCompensGz=[]
        
        # NIVEL DC
        self.QuitarAxu=[0.0,0.0,0.0]

        self.Covarianza=[]
        
        print("Leere Sus Datos Ingeniero")
    
    
    # FUNCION LECTURA DE DATOS
    def LeerDatoActual(self):
        try:
            while True:

                if (self.datosSerial.inWaiting()>0):

                    # LECTURA DE LOS VALORES - SEPARACION
                    datos = self.datosSerial.readline().decode('utf-8')
                    datos = datos.replace('\r\n', ' ')
                    AuxVector=datos.split(sep=',')

                    self.Vector[0]=float(AuxVector[0])
                    self.Vector[1]=float(AuxVector[1])
                    self.Vector[2]=float(AuxVector[2])
                    self.VarianzaAx=0
                    self.VarianzaAy=0
                    self.varianzaGz=0
                    return self.Vector
                
        except :
            print("error en lectura")
            pass
        
    
    # LISTA EJES DE COMPENSACION
    def AgregarLista(self,x,y,z):
        self.ToCompensAx.append(x)
        self.ToCompensAy.append(y)
        self.ToCompensGz.append(z)
    

    # CALCULO DE LA VARIANZA
    def CovarianzaSensores(self,prom):
        
        lista1 = list(repeat(prom[0], len(self.ToCompensAx)))
        lista2 = list(repeat(prom[1], len(self.ToCompensAy)))
        lista3 = list(repeat(prom[2], len(self.ToCompensGz)))

        for variable in range(len(self.ToCompensAx)):

            self.VarianzaAx=self.VarianzaAx+math.pow((self.ToCompensAx[variable]- lista1[variable]),2)
            self.VarianzaAy=self.VarianzaAy+math.pow((self.ToCompensAy[variable]- lista2[variable]),2)
            self.varianzaGz=self.varianzaGz+math.pow((self.ToCompensGz[variable]- lista3[variable]),2)

        self.VarianzaAx=self.VarianzaAx/(len(self.ToCompensAx)-1)
        self.VarianzaAy=self.VarianzaAy/(len(self.ToCompensAy)-1)
        self.varianzaGz=self.varianzaGz/(len(self.ToCompensGz)-1)

        aux=[self.VarianzaAx,self.VarianzaAy,self.varianzaGz]
        # self.Covarianza = np.array ([self.ToCompensAx, self.ToCompensAy, self.ToCompensGz])
        # aux = np.cov (self.Covarianza )

        print(aux)
        print("Estimado Ingeniero la calibracion se realizo con exito")
        time.sleep(2)
        return aux
    
    
    def QuitarNivelDC(self):

        self.QuitarAxu[0]=statistics.mean(self.ToCompensAx)
        self.QuitarAxu[1]=statistics.mean(self.ToCompensAy)
        self.QuitarAxu[2]=statistics.mean(self.ToCompensGz)
        return self.QuitarAxu


# DATOS

    
    
    # GUARDADO PRUEBA
    #data = np.array(Aux[0])

    # if (n==80):

    #     CompensacionCovarianza.CovarianzaSensores
    #     # PRIMERA
    #     cov_mat = Datos[0].cov()
    #     print("Covarianza Eje X ONE: ")
    #     print(cov_mat)

    #     # SEGUNDA
    #     COV = np.cov(Datos[0])
    #     print("Covarianza Eje X dos: ")
    #     print(COV)








# '''
        

#         # PRUEBA INCIAL
#         lectura_Lista.append(datos)

#         # SEPARANDO
#         # lectura_Lista = x.split(",") #COMPROBAR QUE POSICION CORRESPONDE CADA EJE x[1]
#         # VarEjeX = lectura_Lista[0] 
#         # VarEjeY = lectura_Lista[1] 
#         # VarGz = lectura_Lista[2] 

#         # SEPARACION DE LOS EJES
#         contador  = contador + 1
            
#         # COMPENSACION DEL SENSOR 
#         if(contador == 120):
#             print("a) Compensacion")
#         '''


   

