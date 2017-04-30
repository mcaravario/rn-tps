import numpy as np
import random


class RN:
    random_funct = lambda: random.uniform(-1.0, 1.0)
    def __init__(self, gs, **kwargs):
        """ Construye la red neuronal

            gs: Lista de funciones de activación por capa
            Ws: Si se pasa se inicializa los pesos con las matrices en el
            ns: Arquitectura de la red.
            biased: Si es True ya estan considerados los pesos de bias,
                    de lo contrario agrega las entrada/pesos del bias en cada capa correspondiente.
                    De forma predeterminada es false.
            Ejemplo:
              n = rn.RN(ns=[3,2,1]) es una red con 3 capas
              (considerando a la de entrada como una capa)
              que tienen 3, 2, 1 neuronas cada capa respectivamente

            Aclaración: Se deben introducir al menos ns o Ws de lo contrario dara error
            y si se proveen los dos, solo leera Ws
        """
        self.gs = gs
        if 'Ws' in kwargs:
            self.Ws = kwargs['Ws']
            if 'biased' in kwargs and (not kwargs['biased']):
                raise Exception("Se especifico que no estaba con bias pero se paso la matriz")

        elif 'ns' in kwargs:
            ns = kwargs['ns']
            self.biased = kwargs.get('biased') or False

            self.random_funct = kwargs.get('random_funct') or RN.random_funct

            def gen_weights(inputs, outputs):
                return np.array([[self.random_funct() for _ in range(inputs)] for _ in range(outputs)])

            if self.biased:
                self.Ws = [gen_weights(ns[i],ns[i+1]) for i in range(len(ns)-1)]
            else:
                self.Ws = [gen_weights(ns[i+1]+1, ns[i]+1) for i in range(len(ns)-2)] + [gen_weights(ns[-2]+1, ns[-1])]
        else:
            raise Exception("Se esperaba las matrices de pesos o la arquitectura")

        if len(self.Ws) != len(self.gs):
            raise Exception("Se esperaba la misma cantidad de funciones que de capas")

    def error_training(self, training):
        error = 0.0
        for x,y in training:
            error += self.get_error(x,y)
        return error / len(training)

    def weights(self):
        """ Devuelve los pesos """
        return self.Ws

    @property
    def nr_layers(self):
        return len(self.Ws)

    def eval(self, x):
        """ Alimenta la red neuronal con entrada x
            y devuelva la salida en formato vector columna"""
        y = list(x)
        if not self.biased:
            y.insert(0, 1.0)
        y = np.array(y).reshape((self.Ws[0].shape[1], 1))
        for W, g in zip(self.Ws, self.gs):
            y = g(np.dot(W, y))
        return y.flatten()

    def get_error(self, x, y):
        error = sum(float(x-y)**2 for x, y in zip(self.eval(x),y))
        return error
