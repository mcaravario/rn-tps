#!/usr/bin/python2

import random
import numpy as np
from numpy import random as npr

def feed_rn(w,x, g=np.sign):
    n = len(x)
    x = np.array(x).reshape((n, 1))
    return g(np.dot(w.T, x))

def learn_rn(xs, ys, epochs=100, eta=0.3):
    def d(y):
        return 1 if y else -1

    # Agrega bias
    xs = list(map(lambda x: [1]+x, xs))

    n = len(xs[0])
    w = npr.random((n, 1))
    for epoch in range(epochs):
        for i in range(len(xs)):
            x = np.array(xs[i]).reshape((n, 1))
            y = ys[i]

            w += (eta * (d(y) - np.sign(np.dot(w.T, x)))) * x
        random.shuffle(xs)
    return w

xs = [[0,0], [0,1], [1,0], [1, 1]]
ys = [ 0,    0,      0,    1 ]
EPOCHS=10
ETA=0.6

w = learn_rn(xs, ys, epochs=EPOCHS, eta=ETA)
print(w)
