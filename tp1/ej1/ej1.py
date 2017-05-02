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

def load_training_validation(training_prop=0.6):
    TRAINING_DB = r'tp1/ej1/data/tp1_ej1_training.csv'
    df = pd.read_csv(TRAINING_DB, header=None)

    outputs = map(lambda x: [1] if x == 'B' else [-1], df[df.columns[0]].as_matrix())
    inputs = df[df.columns[1:]].as_matrix()

    data = list(zip(inputs, outputs))

    training_size = math.floor(training_prop * len(data))

    choices = [1 for i in range(training_size)] + [0 for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: 1-x, choices)))

    return training, validation

def porcentaje_aciertos(rn, data):
    res = 0
    for x,y in data:
        if rn.eval(x) == y:
            res += 1
    return res / len(data)


training, validation = load_training_validation(0.8)
normalize = stat.norm_training_funct(training)
training = list(map(normalize, training))
validation = list(map(normalize, validation))

def random_funct(inputs, outputs):
    r = 4 * math.sqrt(6.0/(inputs+outputs))
    return random.uniform(-r, r)

def entrenar_nueva_red():
    red = RN(ns=[10, 8, 4, 2, 1], gs=[af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sign()])
    tutor = lm.BackPropagation(red)
    for epoch, error in tutor.learn(training,
                                    training_mode=lm.TrainMode.MINI_BATCH,
                                    batch_size=20,
                                    epochs=500,
                                    eta=0.1):
        p_aciertos_t = porcentaje_aciertos(red, training)
        p_aciertos_v = porcentaje_aciertos(red, validation)
        print("{}\t{}\t{}".format(epoch, p_aciertos_t, p_aciertos_v))

entrenar_nueva_red()
