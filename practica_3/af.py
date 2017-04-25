import numpy as np
import math

def vectorize_af(gen_f):
    def g(*args, **kwargs):
        f = gen_f(*args, **kwargs)
        nf = np.vectorize(f)
        nf.dif = np.vectorize(f.dif)
        return nf
    return g

def attach_diff(derivative):
    def wrapper(gen_f):
        def g(*args, **kwargs):
            f = gen_f(*args, **kwargs)
            f.dif = derivative(*args, **kwargs)
            return f
        return g
    return wrapper


@vectorize_af
@attach_diff(lambda: lambda x: 1)
def sign():
    return lambda x: 1 if x >= 0 else -1

def sig(x):
    return 1.0 / (1.0 + math.exp(-x))

@vectorize_af
@attach_diff(lambda beta: lambda x: 2 * beta * sig(2*beta*x) * (1.0 - sig(2*beta*x)))
def sigmoid(beta=0.5):
    return lambda x: sig(2*beta*x)
