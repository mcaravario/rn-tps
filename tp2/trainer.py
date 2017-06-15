import numpy as np
import abc

class Trainer:
    def __init__(self, rn):
        self.rn = rn

    @abc.abstractmethod
    def fit(self, x, eta):
        pass

    def fit_train(self, eta, train):
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
        y_predict = self.rn.eval(x)
        delta = np.zeros(self.rn.w.shape)

        for j in range(delta.shape[0]):
            for i in range(delta.shape[1]):
                delta[j][i] = eta * y_predict[j][0] * (x[i] - sum(self.rn.w[k][i] * y_predict[k][0] for k in range(0,j)))

        self.rn.w += delta
