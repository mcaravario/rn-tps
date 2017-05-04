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
    TRAINING_DB = r'tp1/ej2/data/tp1_ej2_training.csv'
    df = pd.read_csv(TRAINING_DB, header=None)

    outputs = map(lambda x: [x], df[df.columns[0]].as_matrix())
    inputs = df[df.columns[1:]].as_matrix()

    data = list(zip(inputs, outputs))

    training_size = math.floor(training_prop * len(data))

    choices = [True for i in range(training_size)] + [False for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: 1-x, choices)))

    return training, validation

training, validation = load_training_validation(0.6)
norm_funct = get_normalization_function(training)
training = list(map(norm_funct, training))
validation = list(map(norm_funct, training))

def random_funct(inputs, outputs):
    r = 4 * math.sqrt(6.0/(inputs+outputs))
    return random.uniform(-r, r)

def entrenar_nueva_red():
    # print(training)
	print(len(training))
	print(len(validation))
    red = RN(ns=[9, 20, 1], gs=[af.tanh(), af.identity()])
    tutor = lm.BackPropagation(red)
    for epoch, error in tutor.learn(training,
                                    training_mode=lm.TrainMode.STOCHASTIC,
                                    epochs=1000,
                                    eta=0.02):
        print("{}\t{}".format(epoch, error))
    print(len(training))

entrenar_nueva_red()
