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
from tp1.utils import get_normalization_function, load_training_validation
from tp1.argv_parser import parse_argv
from tp1.rn import RN

def experimentar(training, validation, red, learn_funct, learn_params):
    for epoch, error_training in learn_funct(training,
                                             **learn_params):
        error_validation = red.error_training(validation)
        aciertos_training, fp_training, fn_training  = porcentaje_aciertos(red, training)
        aciertos_validation, fp_validation, fn_validation  = porcentaje_aciertos(red, validation)
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(epoch,
                                          error_training,
                                          error_validation,
                                          aciertos_training,
                                          aciertos_validation,
                                          fp_validation,
                                          fn_validation))
def main():
    arguments = parse_argv()
    training, validation = load_training_validation(r'tp1/ej1/data/tp1_ej1_training.csv', input_series=pd.Series(range(11)[1]))

    if arguments['normalize_input'] or arguments['normalize_output']:
        norm_funct = get_normalization_function(training,
                                                arguments['normalize_input'],
                                                arguments['normalize_output'])
        training = list(map(norm_funct, training))
        validation = list(map(norm_funct, training))

    experimentar(training, validation, arguments['red'], arguments['learn_funct'], arguments['learn_params'])

if __name__ == '__main__':
    main()
