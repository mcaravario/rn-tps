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

class SOM:
    def __init__(self, inputs, rows, columns):
        self.inputs = inputs
        self.rows = rows
        self.columns = columns
        self.w = npr.random((rows, columns, inputs))

    def dist(self, i, j, x):
        return np.linalg.norm(self.w[i][j]-x)

    def winner(self, x):
        x = np.array(x).flatten()
        min_i = min_j = 0
        min_dist = self.dist(min_i, min_j, x)

        for i in range(self.rows):
            for j in range(self.columns):
                d = self.dist(i, j, x)
                if min_dist > d:
                    min_i = i
                    min_j = j
                    min_dist = d
        return min_i, min_j
