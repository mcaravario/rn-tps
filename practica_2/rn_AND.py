#!/usr/bin/python3
import sys

from rn import PerceptronSimple

def test_rn_AND(epoch=1, eta=0.3):
    xs = [[0,0], [0,1], [1,0], [1, 1]]
    ys = [ 0,    0,      0,    1 ]

    rn_AND = PerceptronSimple(2)
    rn_AND.learn(xs, ys, epochs=epochs, eta=eta)

    print(rn_AND.w)

    for x in xs:
        print("{} -> {}".format(x, rn_AND.eval(x)))

if len(sys.argv) > 1:
    epochs=int(sys.argv[1])
else:
    epochs=1

if len(sys.argv) > 2:
    eta=float(sys.argv[2])
else:
    eta=0.3

test_rn_AND(epochs, eta)
