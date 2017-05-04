#!/bin/python3
import numpy as np
import rn
import af
import lm
from utils import get_normalization_function

def training(n):
    if n == 0:
        yield ([], [1])
    else:
        for x, y in training(n-1):
            z = y[0]
            yield (x+[0],[z])
            yield (x+[1],[-z])

def test_parity(n):
    train = list(training(n))
    norm_funct = get_normalization_function(train)
    # train = list(map(norm_funct, train))
    # xs, ys = zip(*train)
    # print(np.mean(xs, axis=0))
    # print(np.std(xs, axis=0))
    nn = rn.RN(ns=[n,2*n,1],gs=[af.sign(), af.sign()])
    l_bp = lm.BackPropagation(nn)
    for epoch, error in l_bp.learn(training=train, epochs=1000, eta=0.02, training_mode=lm.TrainMode.STOCHASTIC):
        print("{}\t{}".format(epoch, error))

test_parity(2)
