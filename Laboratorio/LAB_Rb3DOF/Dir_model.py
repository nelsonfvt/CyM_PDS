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

def Dir_model(T):
    a = np.array([0.0, 10.0, 10.0])
    d = np.array([0.0, 0.0, 0.0])
    alp = np.array([math.pi/2, 0.0, 0.0])

    A01 = Mx_hgne(a[0], d[0], alp[0],T[0])
    A12 = Mx_hgne(a[1], d[1], alp[1],T[1])
    A23 = Mx_hgne(a[2], d[2], alp[2],T[2])

    A03 = np.matmul(np.matmul(A01,A12),A23)

    return A03[0:3,3]

T = np.array([0.0, 0.0, 0.0])

for i in range(1, len(sys.argv)):
    T[i-1] = float(sys.argv[i])

print(Dir_model(T))