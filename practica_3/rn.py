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
         delta = [None for i in range(len(vs))]
         deltas[-1] = gs[-1][1](vs[-1][0]) * (y - vs[-1][1]))
         for m in (range(len(vs)-2, 0, -1):
             for i in range(self.Ws.shape[1]):
                 delta[i] = gs[m][1](vs[m][0][i]) * sum(z((Ws[m+1][j][i] * deltas[m+1][j])  for j in range(len(self.Ws.shape[0]))))

            delta = gs[m][1](vs[m][0]) * sumatoria (Ws[m+1].T * deltas[m+1])
            deltas[m] = delta
