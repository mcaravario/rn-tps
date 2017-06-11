#!usr/bin/python3

import random
import numpy as np
import abc
from numpy import random as npr

class RN:

    def __init__(self, inputs, outputs):
        self.n = inputs
        self.w = npr.random((outputs, self.n))

    def eval(self, x):
        # Si la entrada esta no viene con bias
        x = np.array(x).reshape((self.n, 1))

        # Realiza el proceso sinaptico
        return np.dot(self.w, x)
