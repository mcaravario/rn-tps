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
from tp1.ej1 import best_network


def porcentaje_aciertos(rn, data):
    res = 0
    errors = 0
    fp = 0
    fn = 0
    for x,y in data:
        if rn.eval(x) == y:
            res += 1
        elif rn.eval(x) == [1] and y == [-1]: # Falso negativo: Te dice que es benigno cuando es maligno
            errors += 1
            fn += 1
        else: # Falso positivo: Te dice que es maligno cuando es benigno
            errors += 1
            fp += 1
    if errors == 0:
        fp = 0
        fn = 0
    else:
        fp = fp / errors
        fn = fn / errors
    return res / len(data) * 100.0, fp * 100.0, fn * 100.0

def entrenar(training, validation, red, learn_funct, learn_params):
    best_Ws = None
    best_ecm_v = None
    best_fn = None
    for epoch, error_training in learn_funct(training,
                                             **learn_params):
        error_validation = red.error_training(validation)
        aciertos_training, fp_training, fn_training  = porcentaje_aciertos(red, training)
        aciertos_validation, fp_validation, fn_validation  = porcentaje_aciertos(red, validation)

        if best_ecm_v is None or \
           (best_ecm_v > error_validation) or \
           (best_ecm_v == error_validation and best_fn > fn_validation):
            best_Ws = red.weights()
            best_ecm_v = error_validation
            best_fn = fn_validation

        print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(epoch,
                                          error_training,
                                          error_validation,
                                          aciertos_training,
                                          aciertos_validation,
                                          fp_validation,
                                          fn_validation))
    return best_Ws

def evaluar(test):
    red = best_network.red
    avg_xs, std_xs, avg_ys, std_ys = best_network.avg_std
    norm_funct = lambda x: normalize(avg_xs, std_xs, avg_ys, std_ys, x)
    test = list(map(norm_funct, test))
    ecm = red.error_training(test)
    aciertos, fp, fn = porcentaje_aciertos(red, test)
    print("ECM: {}".format(ecm))
    print("Aciertos: {}".format(aciertos))
    print("Falsos Positivos: {}".format(fp))
    print("Falsos Negativos: {}".format(fn))


def main():
    def to_bipolar(d):
        x = d[0]
        y = d[1]
        return (x, [1.0] if y == 'B' else [-1.0])

    arguments = parse_argv(0)
    output_series = pd.Series([0])
    input_series = pd.Series([1, 2,3,4,5,6,7,8,9,10])
    data = load_database(arguments['db'], input_series, output_series)
    data = list(map(to_bipolar, data))

    if not arguments['train']:
        evaluar(data)
        return

    training, validation = split_training_validation(data, training_prop=arguments['training_prop'])


    avg_xs, std_xs, avg_ys, std_ys = get_avg_std(training,
                                                 arguments['normalize_input'],
                                                 False)
    norm_funct = lambda x: normalize(avg_xs, std_xs, avg_ys, std_ys, x)
    training = list(map(norm_funct, training))
    validation = list(map(norm_funct, validation))


    best_Ws = entrenar(training, validation, arguments['red'], arguments['learn_funct'], arguments['learn_params'])
    if arguments['output']:
        with open(arguments['output'], 'w+') as f:
            f.write("red = rn.RN(Ws={})\n".format(best_Ws))
            f.write("avg_std = ({},{},{},{})\n".format(avg_xs, std_xs, avg_ys, std_ys))

main()
