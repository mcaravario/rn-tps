import numpy as np
import math

def vectorize_af(gen_f):
    def g(*args, **kwargs):
        f = gen_f(*args, **kwargs)
        nf = np.vectorize(f)
        return nf
    return g

@vectorize_af
def sign():
    return lambda x: 1 if x >= 0 else -1

def sig(x):
    return 1.0 / (1.0 + math.exp(-x))

@vectorize_af
def sigmoid(beta=0.5):
    return lambda x: sig(2*beta*x)
