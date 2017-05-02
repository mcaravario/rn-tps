#!/usr/bin/python3

from itertools import compress
from pandas import DataFrame, read_csv
import math
import random
import numpy as np
import pandas as pd
import sys

from tp1 import lm
from tp1 import af
from tp1 import stat
from tp1.rn import RN

def load_training_validation():
    TRAINING_DB = r'tp1/ej1/data/tp1_ej1_training.csv'
    df = pd.read_csv(TRAINING_DB, header=None)

    outputs = map(lambda x: [1] if x == 'B' else [-1], df[df.columns[0]].as_matrix())
    inputs = df[df.columns[1:]].as_matrix()

    data = list(zip(inputs, outputs))

    training_prop = 0.6

    training_size = math.floor(training_prop * len(data))

    choices = [1 for i in range(training_size)] + [0 for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: 1-x, choices)))

    return training, validation


training, validation = load_training_validation()

normalize = stat.norm_training_funct(training)
training = list(map(normalize, training))
validation = list(map(normalize, validation))


red = RN(ns=[10, 10, 8, 5, 1], gs=[af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sign()])
print(red.weights())
tutor = lm.BackPropagation(red)
errors = tutor.learn(training,
                     training_mode=lm.TrainMode.STOCHASTIC,
                     epochs=1,
                     eta=0.01)
# error_valid = red.error_training(validation)

print(errors[-1])
print(min(errors))

acierta_training = 0
acierta_validation = 0
for x,y in training:
    if red.eval(x) == y:
        acierta_training += 1

for x,y in validation:
    if red.eval(x) == y:
        acierta_validation += 1

print(acierta_training / len(training) * 100.0)
print(acierta_validation / len(validation) * 100.0)
