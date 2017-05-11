import numpy as np
import math
import random
import pandas as pd
import sys
from itertools import compress


def get_normalization_function(training, normalize_input=True, normalize_output=False):
    xs, ys = zip(*training)
    if normalize_input:
        avg_xs = np.mean(xs, axis=0)
        std_xs = np.std(xs, axis=0)
    else:
        avg_xs = np.zeros(len(xs))
        std_xs = np.ones(len(xs))

    if normalize_output:
        avg_ys = np.mean(ys, axis=0)
        std_ys = np.std(ys, axis=0)
    else:
        avg_ys = np.zeros(len(ys))
        std_ys = np.ones(len(ys))

    def t(xy):
        x = xy[0]
        y = xy[1]
        rx = [0.0 for i in range(len(x))]
        ry = [0.0 for i in range(len(y))]
        for i in range(len(x)):
            if std_xs[i] != 0:
                rx[i] = (x[i] - avg_xs[i])/std_xs[i]
        for i in range(len(y)):
            if std_ys[i] != 0:
                ry[i] = (y[i] - avg_ys[i])/std_ys[i]
        return (rx, ry)
    return t

def load_training_validation(training_db, input_series, output_series, training_prop=0.6):
    df = pd.read_csv(training_db, header=None)

    outputs = df[output_series].as_matrix()
    inputs = df[input_series].as_matrix()

    data = list(zip(inputs, outputs))

    training_size = int(training_prop * len(data))

    choices = [True for i in range(training_size)] + [False for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: not x, choices)))

    return training, validation
