import sys
import numpy as np
import math

def Dir_model(T):
    a = np.array([0.0, 10.0, 10.0])

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

    return A03[0:3,3]

T = np.array([0.0, 0.0, 0.0])

for i in range(1, len(sys.argv)):
    T[i-1] = float(sys.argv[i])

print(Dir_model(T))