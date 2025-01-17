import numpy as np
import csv

N = 4
xn = np.array(np.zeros(N))
yn = np.array(np.zeros(N))

num = np.array([0.0316893438497110,	0.0950680315491331,	0.0950680315491331,	0.0316893438497110])
den = np.array([1,	-1.45902906222806,	0.910369000290069,	-0.197825187264319])

with open('samples_1.csv') as csvfile:
    samples = csv.reader(csvfile)
    for row in samples:
        y = 0
        for i in range(N-1, 0, -1):
            xn[i] = xn[i-1]
            yn[i] = yn[i-1]
            y = y + num[i] * xn[i] - den[i] * yn[i]
        
        xn[0] = float(row[0])
        y = y + num[0] * xn[0]
        yn[0] = y

        print(y)