import numpy as np

def vectorize_af(gen_f):
    def g(*args, **kwargs):
        f = gen_f(*args, **kwargs)
        nf = np.vectorize(f)
        nf.dif = np.vectorize(f.dif)
        return nf
    return g

@vectorize_af
def identity():
	f = lambda x: x
	f.dif = lambda x: 1.0
	return f

@vectorize_af
def ReLu():
	f = lambda x: x if x > 0 else 0.0
	f.dif = lambda x: 1.0 if x > 0 else 0.0
	return f

@vectorize_af
def sign():
    f = lambda x: 1.0 if x > 0.0 else -1.0
    f.dif = lambda x: 1.0
    return f

@vectorize_af
def sigmoid(beta=0.5):
    def f(x):
        try:
            return 1.0 / (1.0 + np.exp(-2.0 * beta * x))
        except OverflowError:
            if x > 0:
                return 1.0
            else:
                return -1.0


    def f_dif(x):
        try:
            y = f(2.0 * beta * x)
            return 2.0 * beta * y * (1 - y)
        except OverflowError:
            return 0.0

    f.dif = f_dif

    return f

@vectorize_af
def tanh(beta=0.5):
    f = lambda x: np.tanh(2.0 * beta * x)
    f.dif = lambda x: 2.0 * beta / ((2.0 * beta * x)**2 + 1.0)
    return f
