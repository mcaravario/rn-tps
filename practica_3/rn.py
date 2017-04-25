import numpy as np


class RN:
    random_funct = np.random
    def __init__(self, gs, **kwargs):
        self.gs = gs
        if 'Ws' in kwargs:
            self.Ws = kwargs['Ws']
        elif 'ns' in kwargs:
            if 'random_funct' in kwargs:
                self.random_funct = kwargs['random_funct']
            self.Ws = [None for i in range(len(ns)-1)]
            for i in range(len(ns)-1)
                self.Ws = np.from_function(lambda _, _: self.random_funct(), (ns[i+1],ns[i]))
        else:
            raise Exception("Se esperaba las matrices de pesos o la arquitectura")

    def weights(self):
        return self.Ws

    def eval(self, x):
        x = np.array(x).reshape((n, 1))
        for W, g in zip(self.Ws, self.gs):
            x = (g(W * x)).T
