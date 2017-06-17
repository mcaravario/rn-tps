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
        outputs = self.rn.w.shape[0]
        x = np.array(x).reshape((self.rn.n, 1))

        y_predict = self.rn.eval(x)

        triangular = np.triu(np.ones((outputs, outputs)))
        delta = x - np.dot(self.rn.w.T, np.multiply(triangular, y_predict))
        delta = eta * (np.multiply(delta, y_predict.T)).T

        self.rn.w += delta
