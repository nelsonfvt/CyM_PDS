import sys
import numpy as np
import math

a = np.array([10.0, 10.0])
Angs = np.array([0.0, 0.0])

EF = np.array([20.0, 0.0]) # Posicion punto final

c2 = (EF[0]**2 + EF[1]**2 -a[0]**2 -a[1]**2) / (2 * a[0] * a[1])
Angs[1] = np.arccos(c2)

alf = np.arctan2(EF[1],EF[0])
bet = np.arccos( (a[0] + a[1]*c2) / (np.sqrt( EF[0]**2 + EF[1]**2 )) )

Angs[0] = alf-bet

print(Angs)