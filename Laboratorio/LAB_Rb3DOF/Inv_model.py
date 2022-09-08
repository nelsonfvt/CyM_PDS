import sys
import numpy as np
import math

def Inv_model(EF):
    a = np.array([0.0, 10.0, 10.0])
    T = np.array([0.0, 0.0, 0.0])

    T[0] = np.arctan2(EF[1], EF[0])

    c3 = ( EF[0]**2 + EF[1]**2 + EF[2]**2 -a[1]**2 -a[2]**2 ) / (2 * a[1] * a[2])
    s3 = math.sqrt(1 - c3**2)
    T[2] = np.arctan2(s3, c3)

    s2 = ( (a[1]+a[2]*c3)*EF[2] - a[2]*s3*math.sqrt(EF[0]**2 + EF[1]**2) ) / (EF[0]**2 + EF[1]**2 + EF[2]**2)
    c2 = ( (a[1]+a[2]*c3)*math.sqrt(EF[0]**2 + EF[1]**2 + a[2]*s3*EF[2]) ) / (EF[0]**2 + EF[1]**2 + EF[2]**2)
    T[1] = np.arctan2(s2, c2)

    return T


EF = np.array([20.0, 0.0, 0.0])

for i in range(1, len(sys.argv)):
    EF[i-1] = float(sys.argv[i])

print(Inv_model(EF))