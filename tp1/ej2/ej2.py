#!/usr/bin/python3

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
    # print("-".join(map(str,red.ns)))
    # print(str(learn_params))
    for epoch, error_training in learn_funct(training,
                                             **learn_params):
        error_validation = red.error_training(validation)
        print("{}\t{}\t{}".format(epoch,
                                  error_training,
                                  error_validation))

def main():
    arguments = parse_argv()
    output_series = pd.Series([8, 9])
    input_series = pd.Series([0,1,2,3,4,5,6,7])
    training, validation = load_training_validation(r'tp1/ej2/data/tp1_ej2_training.csv', input_series, output_series, training_prop=arguments['training_prop'])

    if arguments['normalize_input'] or arguments['normalize_output']:
        norm_funct = get_normalization_function(training,
                                                arguments['normalize_input'],
                                                arguments['normalize_output'])
        training = list(map(norm_funct, training))
        validation = list(map(norm_funct, validation))

    experimentar(training, validation, arguments['red'], arguments['learn_funct'], arguments['learn_params'])

main()
