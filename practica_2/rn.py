#!/usr/bin/python3

import random
import numpy as np
from numpy import random as npr

EPOCHS = 1
ETA = 0.3

class RN:
    g = lambda x: x

    def __init__(self, n):
        self.n = n + 1
        self.w = npr.random((1, self.n))

    def eval(self, x, biased=False):
        # Si la entrada esta no viene con bias
        if not biased:
            x = np.array([1] + x).reshape((self.n, 1))
        else:
            x = np.array(x).reshape((self.n, 1))

        # Realiza el proceso sinaptico
        return self.g(np.dot(self.w, x))[0][0]

    def learn(self, xs, ys, eta=ETA, epochs=EPOCHS):
        # Agrega bias a la entrada
        xs = list(map(lambda x: [1]+x, xs))
        zs = list(zip(xs, ys))

        for epoch in range(epochs):
            self.learn_one_epoch(xs, ys, eta=eta)
            random.shuffle(zs)
            xs, ys = zip(*zs)

class PerceptronSimple(RN):
    g = np.sign

    def __init__(self, n=None):
        super(PerceptronSimple, self).__init__(n)

    def learn_one_epoch(self, xs, ys, eta=ETA):
        def d(y):
            return 1 if y else -1

        for i in range(len(xs)):
            x = np.array(xs[i]).reshape((self.n, 1))

            error = d(ys[i]) - self.eval(x, biased=True)

            self.w += eta * error * x.T

xs = [[0,0], [0,1], [1,0], [1, 1]]
ys = [ 0,    0,      0,    1 ]
epochs=1000
eta=0.2

rn_AND = PerceptronSimple(2)
rn_AND.learn(xs, ys, epochs=epochs, eta=eta)

print(rn_AND.w)

for x in xs:
    print("{} -> {}".format(x, rn_AND.eval(x)))
