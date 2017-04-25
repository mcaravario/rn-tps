import numpy as np
import math
def sign():
    return lambda x: 1 if x >= 0 else -1

def sig(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid(beta=0.5):
    return lambda x: sig(2*beta*x)
