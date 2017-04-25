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
        deltas = []
        # g'(h_i(M) * [error])
        # W = salidas * entradas
        # delta = 
        y = np.array(y).reshape((self.Ws[-1][0], 1))

        last_layer = -1

        delta = np.zeros((self.Ws[-1].shape[0], 1))
        for i in range(self.Ws[last_layer].shape):
            g = gs[last_layer]
            h = vs[last_layer][0]
            V = vs[last_layer][1]
            delta[i] = g.dif(h[i]) * (y - V[i])

        delta_W = eta * delta * self.vs[last_layer-1].T
        W[last_layer] += delta_W

        for m in (range(len(vs)-2, 0, -1):
            g = gs[m]
            h = vs[m][0]
            for i in range(self.Ws.shape[1]):
                delta[i] = g.dif(h[i]) * self.Ws.T * delta
            V = vs[m+1][1]
            delta_W = eta * delta * V.T
            W = W + delta_W
