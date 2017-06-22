import numpy as np
import abc

class Trainer:
    ETA = 0.0001

    def __init__(self, rn):
        self.rn = rn

    @abc.abstractmethod
    def fit(self, x, eta):
        pass

    def fit_train(self, train, epochs, eta=ETA):
        for epoch in range(epochs):
            for instance in train:
                self.fit(instance, eta)

class Oja(Trainer):

    def __init__(self, rn):
        self.rn = rn

    def fit(self, x, eta):

        x = np.array(x).reshape((self.rn.n, 1))
        y_predict = self.rn.eval(x)

        delta = eta * np.dot(y_predict, (x - np.dot(self.rn.w.T, y_predict)).T)
        self.rn.w += delta

class Sanger(Trainer):

    def __init__(self, rn):
        self.rn = rn

    def fit(self, x, eta):
        outputs = self.rn.w.shape[0]
        x = np.array(x).reshape((self.rn.n, 1))

        y_predict = self.rn.eval(x)

        triangular = np.triu(np.ones((outputs, outputs)))
        delta = x - np.dot(self.rn.w.T, np.multiply(triangular, y_predict))
        delta = eta * (np.multiply(delta, y_predict.T)).T

        self.rn.w += delta

class SOMTrainer(Trainer):
    ETA = 0.001
    SIGMA = 0.01
    dist_map = lambda x: np.exp(-x**2/2)
    cooling_fn = lambda x: np.exp(-x)

    def __init__(self,
                 rn,
                 dist_map = None,
                 cooling_fn = None,
                 ):
        self.rn = rn
        self.dist_map = dist_map or SOMTrainer.dist_map
        self.cooling_fn = cooling_fn or SOMTrainer.cooling_fn

    def fit(self, x, eta=ETA, sigma=SIGMA):
        w_i, w_j = self.rn.winner(x)

        def h(i, j):
            d = np.linalg.norm(((i-w_i),(j-w_j)))
            return self.dist_map(d/sigma)

        for i in range(self.rn.rows):
            for j in range(self.rn.columns):
                self.rn.w[i][j] += eta * h(i, j) * (x-self.rn.w[i][j])

    def fit_train(self, train, epochs, eta0=ETA, sigma0=ETA, tao0=1, tao1=1):
        t = 0
        for e in range(epochs):
            for x in train:
                eta = eta0 * self.cooling_fn(t/tao0)
                sigma = sigma0 * self.cooling_fn(t/tao1)

                self.fit(x, eta, sigma)
                t += 1
