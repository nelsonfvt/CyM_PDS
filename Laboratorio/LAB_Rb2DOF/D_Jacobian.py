import numpy as np
def D_Jacobian(q,l):
    J_a = np.array([[-l[0]*np.sin(q[0]) - l[1]*np.sin(q[0]+q[1]) , -l[1]*np.sin(q[0]+q[1])],
                    [l[0]*np.cos(q[0]) + l[1]*np.cos(q[0]+q[1]), l[1]*np.cos(q[0]+q[1])]])
    return J_a