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
from tp1.utils import get_normalization_function
from tp1.rn import RN

def load_training_validation(training_prop=0.6):
    TRAINING_DB = r'tp1/ej1/data/tp1_ej1_training.csv'
    df = pd.read_csv(TRAINING_DB, header=None)

    outputs = map(lambda x: [1] if x == 'B' else [-1], df[df.columns[0]].as_matrix())
    inputs = df[df.columns[1:]].as_matrix()

    data = list(zip(inputs, outputs))

    training_size = math.floor(training_prop * len(data))

    choices = [True for i in range(training_size)] + [False for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: not x, choices)))

    return training, validation

def porcentaje_aciertos(rn, data):
    res = 0
    for x,y in data:
        if rn.eval(x) == y:
            res += 1
    return res / len(data)


training, validation = load_training_validation(0.6)
norm_funct = get_normalization_function(training)
training = list(map(norm_funct, training))
validation = list(map(norm_funct, validation))

def entrenar_nueva_red():
    red = RN(ns=[10, 7, 1], gs=[af.sigmoid(), af.sign()])
    tutor = lm.BackPropagation(red)
    for epoch, error in tutor.learn(training,
                                    training_mode=lm.TrainMode.STOCHASTIC,
                                    epochs=1000,
                                    eta=0.05):
        error_validation = red.error_training(validation)
        aciertos_training = porcentaje_aciertos(red, training)
        aciertos_validation = porcentaje_aciertos(red, validation)
        print("{}\t{}\t{}\t{}\t{}".format(epoch, error, error_validation, aciertos_training * 100, aciertos_validation * 100))

entrenar_nueva_red()
