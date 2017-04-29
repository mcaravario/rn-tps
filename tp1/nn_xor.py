#!/bin/python3

import rn
import af
import lm

def test_XOR(epochs=500, mode='stochastic', batch_size=1):
    training = [([1,0,0],[-1]),
                ([1,0,1],[1]),
                ([1,1,0],[1]),
                ([1,1,1],[-1])]
    nn_xor = rn.RN(ns=[3,3,1],gs=[af.sign(), af.sign()])
    l_bp = lm.BackPropagationOptimized(nn_xor)
    errors = l_bp.learn_adaptative(training=training, epochs=epochs, eta=0.1, a=0.5, b=0.7, training_mode=mode, batch_size=batch_size)

    return min(errors)

# iters = 50
# epochs= 500
# count_s = 0
# count_b = 0
# for i in range(iters):
#     if test_XOR(epochs=epochs, mode='stochastic') < 0.01:
#         count_s += 1
#     if test_XOR(epochs=epochs, mode='batch') < 0.01:
#         count_b += 1
#
# print("STOCHASTIC = " + str(count_s / iters))
# print("BATCH = " + str(count_b / iters))
