import numpy as np


class RN:
    def __init__(self, ns, gs):
        self.Ws = [ np.random((ns[i+1], ns[i])) for i in range(len(ns)-1) ]
        self.gs = gs

    def eval(self, x):
        x = np.array(x).reshape((n, 1))
        for W, g in zip(self.Ws, self.gs):
            x = (g(W * x)).T

    def forward(self, x):
        vs = []
        x = np.array(x).reshape((n, 1))
        vs.append(x)
        for W, g, _ in zip(self.Ws, self.gs):
            y = (W * x).T
            x = g(y)
            vs.append((y,x))
         return vs

     def backward(self, vs, y, eta=0.3):
        # g'(h_i(M) * [error])
        ######################################################
        ##        W en R^(salidas * entradas)               ##
        ##--------------------------------------------------##
        ##                                                  ##
        ##  W_{i,j} = el peso de la entrada j a la salida i ##
        #####################################################

        last_layer = -1
        # W es la matriz de la ultima capa
        W = self.Ws[last_layer]
        # La ultima capa
        assert(len(y) == W.shape[0])
        # interpretamos y como un vector columna
        y = np.array(y).reshape((W.shape[0], 1))

        delta = np.zeros((W.shape[0], 1))

        g = gs[last_layer]
        h, v = vs[last_layer]
        delta = g.dif(h) * (y - V) # multiplicacion elemento a elemento
        delta_W = eta * delta * self.vs[last_layer-1].T
        W += delta_W

        for m in (range(len(vs)-2, 0, -1):
            W = self.Ws[m]
            delta = np.zeros((W.shape[0], 1))
            g = gs[m]
            h, v = vs[m]

            s = self.Ws.T * delta
            # Multiplicacion elemento a elemento
            delta = g.dif(h) * s

            delta_W = eta * delta * v.T
            W = W + delta_W
