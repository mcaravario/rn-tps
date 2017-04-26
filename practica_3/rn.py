import numpy as np
import random


class RN:
    random_funct = lambda: random.uniform(-1.0, 1.0)
    def __init__(self, gs, **kwargs):
        """ Construye la red neuronal

            gs: Lista de funciones de activación por capa
            Ws: Si se pasa se inicializa los pesos con las matrices en el
            ns: Arquitectura de la red.
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
        elif 'ns' in kwargs:
            ns = kwargs['ns']

            self.random_funct = kwargs.get('random_funct') or RN.random_funct

            def gen_matrix(h, w):
                return np.array([[self.random_funct() for _ in range(w)] for _ in range(h)])

            self.Ws = [ gen_matrix(ns[i+1],ns[i]) for i in range(len(ns)-1) ]
        else:
            raise Exception("Se esperaba las matrices de pesos o la arquitectura")

        if len(self.Ws) != len(self.gs):
            raise Exception("Se esperaba la misma cantidad de funciones que de capas")

    def weights(self):
        """ Devuelve los pesos """
        return self.Ws

    def eval(self, x):
        """ Alimenta la red neuronal con entrada x
            y devuelva la salida en formato vector columna"""
        x = np.array(x).reshape((self.Ws[0].shape[1], 1))
        for W, g in zip(self.Ws, self.gs):
            x = g(np.dot(W, x))
        return x
