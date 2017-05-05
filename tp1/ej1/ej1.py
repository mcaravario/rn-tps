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
    return res / len(data) * 100.0


training, validation = load_training_validation(0.6)
norm_funct = get_normalization_function(training)
training = list(map(norm_funct, training))
validation = list(map(norm_funct, validation))

DIR_EJ1_BASE='tp1/ej1/pruebas/'

# Experimento 1: Variamos capas y cantidad de neuronas
redes_experimento_1 = (RN(ns=[10, 1], gs=[af.sign()]),
                       RN(ns=[10, 5, 1], gs=[af.sigmoid(), af.sign()]),
                       RN(ns=[10, 20, 1], gs=[af.sigmoid(), af.sign()]),
                       RN(ns=[10, 5, 5, 8, 1], gs=[af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sign()]),
                       RN(ns=[10, 15, 20, 5, 1], gs=[af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sign()]),
                       RN(ns=[10, 10, 10, 10, 10, 1], gs=[af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sigmoid(), af.sign()]))

experimento_1 = {'nombre': 'experimento 1',
                 'redes':redes_experimento_1,
                 'parametros':[{'lc':lm.BackPropagation, 'learn_params':{'eta':0.03, 'epochs':500, 'training_mode': lm.TrainMode.STOCHASTIC}}]}

experimentos = [experimento_1]



def experimentar(i):
    experimento = experimentos[i]
    for red in experimento['redes']:
        print(red.ns)
        for params in experimento['parametros']:
            learn_params = params['learn_params']
            tutor = params['lc'](red)
            filename_base = DIR_EJ1_BASE
            filename_base += 'ex_{}_plot_{}_ep_{}_eta_{}.dat'.format(str(i+1), '-'.join(map(str,red.ns)),
                                                              str(learn_params['epochs']),
                                                              str(learn_params['eta']))
            with open(filename_base, 'w+') as f:
                for epoch, error_training in tutor.learn(training,
                                                         **learn_params):
                    error_validation = red.error_training(validation)
                    aciertos_training = porcentaje_aciertos(red, training)
                    aciertos_validation = porcentaje_aciertos(red, validation)
                    print("{}\t{}\t{}\t{}\t{}".format(epoch,
                                                    error_training,
                                                    error_validation,
                                                    aciertos_training,
                                                    aciertos_validation),
                         file=f)
            f.close()


nr_experimento = int(sys.argv[1])
experimentar(nr_experimento)
