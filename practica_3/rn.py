import numpy as np


class RN:
    random_funct = np.random
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
            if 'random_funct' in kwargs:
                self.random_funct = kwargs['random_funct']
            ns = kwargs['ns']
            self.Ws = [None for i in range(len(ns)-1)]
            for i in range(len(ns)-1):
                self.Ws = np.from_function(lambda i, j: self.random_funct(), (ns[i+1],ns[i]))
        else:
            raise Exception("Se esperaba las matrices de pesos o la arquitectura")

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
