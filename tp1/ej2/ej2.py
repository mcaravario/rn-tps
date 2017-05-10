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

    outputs = df[df.columns[-2:]].as_matrix()
    inputs = df[df.columns[:-2]].as_matrix()

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

DIR_EJ2_BASE='tp1/ej2/pruebas/'

def random_funct(inputs, outputs):
	d = float(inputs + outputs)
	sd = math.sqrt(1.0/d)
	return random.uniform(sd, sd)
	

# Experimento 1: Variamos capas y cantidad de neuronas
redes_1 = (RN(ns=[8, 16, 2], gs=[af.sigmoid(), af.identity()]),)
redes_2 = (RN(ns=[8, 16, 2], gs=[af.tanh(), af.identity()]),)
redes_3 = (RN(ns=[8, 16, 4, 2], gs=[af.ReLu(), af.tanh(), af.identity()]),)
redes_4 = (RN(ns=[8, 16, 2], gs=[af.tanh(), af.identity()], random_funct=random_funct), )

params = {'lc':lm.BackPropagation, 'learn_params':{'eta':0.02, 'epochs':500, 'training_mode': lm.TrainMode.STOCHASTIC}}


experimento_1 = {'nombre': 'experimento 1',
                 'redes': redes_1,
                 'parametros':[params]}

experimento_2 = {'nombre': 'experimento 1',
                 'redes': redes_2,
                 'parametros':[params]}

experimento_3 = {'nombre': 'experimento 1',
                 'redes': redes_3,
                 'parametros':[params]}

experimento_4 = {'nombre': 'experimento 1',
                 'redes': redes_4,
                 'parametros':[params]}


experimentos = [experimento_1, experimento_2, experimento_3, experimento_4]

def experimentar(i, j):
    experimento = experimentos[i]
    params = experimento['parametros'][j]
    learn_params = params['learn_params']
    print(";".join(map(str, learn_params.items())))
    for red in experimento['redes']:
        print(red.ns)
        tutor = params['lc'](red)
        filename_base = DIR_EJ2_BASE
        filename_base += 'ex_{}-{}_red_{}'.format(str(i+1),str(j+1),"-".join(map(str, red.ns)))
        with open(filename_base + '.dat', 'w+') as f:
            for epoch, error_training in tutor.learn(training,
                                                     **learn_params):
                error_validation = red.error_training(validation)
                print("{}\t{}\t{}".format(epoch, \
                                          error_training, \
                                          error_validation), file=f)
        f.close()


nr_experimento = int(sys.argv[1])
nr_param =  int(sys.argv[2])
experimentar(nr_experimento, nr_param)
