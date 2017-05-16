#!/usr/bin/python3

import math
import random
import numpy as np
import pandas as pd
import sys

from tp1 import lm
from tp1 import af
from tp1.utils import *
from tp1.argv_parser import parse_argv
from tp1.rn import RN
from tp1.ej2 import best_network

def entrenar(training, validation, red, learn_funct, learn_params):
    best_Ws = None
    best_ecm_v = None
    for epoch, error_training in learn_funct(training,
                                             **learn_params):
        error_validation = red.error_training(validation)

        if best_ecm_v is None or \
           (best_ecm_v > error_validation):
            best_Ws = red.weights()
            best_ecm_v = error_validation

        print("{}\t{}\t{}".format(epoch,
                                  error_training,
                                  error_validation))
    return best_Ws

def evaluar(test):
    red = best_network.red
    avg_xs, std_xs, avg_ys, std_ys = best_network.avg_std
    norm_funct = lambda x: normalize(avg_xs, std_xs, avg_ys, std_ys, x)
    test = list(map(norm_funct, test))
    ecm = red.error_training(test)
    print("ECM: {}".format(ecm))


def main():
    arguments = parse_argv(1)
    output_series = pd.Series([8, 9])
    input_series = pd.Series([0,1,2,3,4,5,6,7])
    data = load_database(arguments['db'], input_series, output_series)

    if not arguments['train']:
        evaluar(data)
        return

    training, validation = split_training_validation(data, training_prop=arguments['training_prop'])

    avg_xs, std_xs, avg_ys, std_ys = get_avg_std(training,
                                                 arguments['normalize_input'],
                                                 arguments['normalize_output'])
    norm_funct = lambda x: normalize(avg_xs, std_xs, avg_ys, std_ys, x)
    training = list(map(norm_funct, training))
    validation = list(map(norm_funct, validation))

    best_Ws = entrenar(training, validation, arguments['red'], arguments['learn_funct'], arguments['learn_params'])
    if arguments['output']:
        with open(arguments['output'], 'w+') as f:
            f.write("red = rn.RN(weights={})\n".format(best_Ws))
            f.write("avg_std = ({},{},{},{})\n".format(avg_xs, std_xs, avg_ys, std_ys))

main()
