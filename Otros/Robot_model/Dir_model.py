import sys
import numpy as np
import math

T = np.array([0, 0, 0])

for i in range(1, len(sys.argv)):
    T[i-1] = float(sys.argv[i])

P = np.array([[0], [0], [0], [1]])
a = np.array([0, 10, 10])

A01 = np.array([[math.cos(T[0]), 0, math.sin(T[0]), 0], 
              [math.sin(T[0]), 0, -math.cos(T[0]), 0 ],
              [0, 1, 0, 0],
              [0, 0, 0, 1]])

A12 = np.array([[math.cos(T[1]), -math.sin(T[1]), 0, a[1]*math.cos(T[1])],
                [math.sin(T[1]), math.cos(T[1]), 0, a[1]*math.sin(T[1])],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

A23 = np.array([[math.cos(T[2]), -math.sin(T[2]), 0, a[2]*math.cos(T[2])],
                [math.sin(T[2]), math.cos(T[2]), 0, a[2]*math.sin(T[2])],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

A03 = np.matmul(np.matmul(A01,A12),A23)

EF = np.matmul(A03,P)
print(EF)