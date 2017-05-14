import numpy as np
import math
import random
import pandas as pd
import sys
from itertools import compress

def random_uniform(inputs, outputs):
    d = 1.0 / math.sqrt(inputs + outputs)
    return random.uniform(-d,d)


def get_avg_std(training, normalize_input=True, normalize_output=False):
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

    return avg_xs, std_xs, avg_ys, avg_ys

def normalize(avg_xs, std_xs, avg_ys, std_ys, xy):
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

def load_database(db, input_series, output_series):
    df = pd.read_csv(db, header=None)

    outputs = df[output_series].as_matrix()
    inputs = df[input_series].as_matrix()

    return list(zip(inputs, outputs))

def split_training_validation(data, training_prop=0.6):
    training_size = int(training_prop * len(data))

    choices = [True for i in range(training_size)] + [False for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: not x, choices)))

    return training, validation
