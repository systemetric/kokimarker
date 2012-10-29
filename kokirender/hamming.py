import numpy as np

G = np.matrix([[1, 1, 0, 1],
               [1, 0, 1, 1],
               [1, 0, 0, 0],
               [0, 1, 1, 1],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])

H = np.matrix([[1, 0, 1, 0, 1, 0, 1],
               [0, 1, 1, 0, 0, 1, 1],
               [0, 0, 0, 1, 1, 1, 1]])

R = np.matrix([[0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 1]])

def encode(l):
    p = np.matrix([l]).T

    tmp = G * p
    output = tmp.A % 2

    return output.T[0]

def syndrome(l):
    r = np.matrix([l]).T

    z = H * r
    output = z.A % 2

    return output.T[0]

def correct(l, z):
    syndrome_val = z[0] + z[1]*2 + z[2]*4

    # no errors, return original
    if (syndrome_val == 0):
        return l

    # flip the error bit
    l[syndrome_val-1] = (l[syndrome_val-1] + 1) % 2

    return l

def decode(l):
    syndrome = syndrome(l)
    corrected = correct(l, syndrome)

    pr = R * np.matrix([corrected]).T

    return pr.T.A[0]
