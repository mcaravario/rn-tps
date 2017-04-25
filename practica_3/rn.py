import numpy as np


class RN:
    def __init__(self, ns, gs):
        self.Ws = [ np.random((ns[i+1], ns[i])) for i in range(len(ns)-1) ]
        self.gs = gs

    def eval(self, x):
        x = np.array(x).reshape((n, 1))
        for W, g in zip(self.Ws, self.gs):
            x = (g(W * x)).T
