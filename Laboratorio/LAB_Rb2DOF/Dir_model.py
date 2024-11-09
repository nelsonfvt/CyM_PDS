import sys
import numpy as np
import math

def Mx_hgne(ai,di,alpi,Ti):
    Mx = np.array([
        [math.cos(Ti), -math.sin(Ti)*math.cos(alpi), math.sin(Ti)*math.sin(alpi), ai*math.cos(Ti)],
        [math.sin(Ti), math.cos(Ti)*math.cos(alpi), -math.cos(Ti)*math.sin(alpi), ai*math.sin(Ti)],
        [0, math.sin(alpi), math.cos(alpi), di],
        [0, 0, 0, 1]])
    return Mx

a = np.array([10.0, 10.0]) #Longitud eslabones
d = np.array([0.0, 0.0])
alp = np.array([0.0, 0.0])

Angs = np.array([0.0, 0.0]) #Angulos articulaciones (radianes)

A01 = Mx_hgne(a[0], d[0], alp[0],Angs[0])
A12 = Mx_hgne(a[1], d[1], alp[1],Angs[1])

A02 = np.matmul(A01,A12)

print(A02[0:2,3])