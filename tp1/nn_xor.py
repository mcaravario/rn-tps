#!/usr/bin/python3

import rn
import af
import lm

def test_XOR(epochs=500, mode=lm.TrainMode.STOCHASTIC, batch_size=1):
    training = [([0,0],[-1]),
                ([0,1],[1]),
                ([1,0],[1]),
                ([1,1],[-1])]
    nn_xor = rn.RN(ns=[2,5,1],gs=[af.sign(), af.sign()])
    l_bp = lm.BackPropagation(nn_xor)
    for epoch, error in l_bp.learn(training=training, epochs=epochs, eta=0.02, training_mode=mode, batch_size=batch_size):
        print("{}\t{}".format(epoch, error))

test_XOR(epochs=200)

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
