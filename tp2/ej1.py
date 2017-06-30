#!/usr/bin/python3
import sys
import numpy as np
import pandas as pd
import argparse
import config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from rn import RN
from trainer import Oja, Sanger, Trainer
from sklearn.decomposition import PCA
from graficar import graficar_componentes


def parser_args():
    parser = argparse.ArgumentParser(description='Entrena una red neuronal auto organizada')
    parser.add_argument('--db', type=str, help="Base de entrenamiento CSV", default=config.DB_TRAINING)
    parser.add_argument('-e', '--epochs', help="Cantidad de epocas", type=int, default=500)
    parser.add_argument('--test-size', help="Proporcion de test en la particion entrenamiento/test", type=float, default=0.2)
    parser.add_argument('--eta', help="Coeficiente eta de aprendizaje", type=float, default=0.001)
    parser.add_argument('--rule', help="Regla utilizada para la reduccion (oja o sanger)", choices=("oja","sanger"), default="oja")
    parser.add_argument('--train', help="Modo entrenamiento", dest='training', action="store_true")
    parser.add_argument('--test', help="Testea la red ya entrenada", dest='training', action="store_false")
    parser.add_argument('--output', help="Salida con los pesos de la red", type=str)
    parser.add_argument('--normalize', help="Normaliza la entrada", dest='normalize', action='store_true')
    parser.add_argument('--no-normalize', help="No normaliza la entrada (defecto)", dest='normalize', action='store_false')
    parser.set_defaults(training=True, normalize=False)
    return parser.parse_args()


def main():

    args = parser_args()
    df = pd.read_csv(args.db, header=None)

    y = df[df.columns[0]]
    X = df[df.columns[1:]].as_matrix()

    if args.normalize:
        X = StandardScaler().fit_transform(X)

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=args.test_size, random_state=42)

    training = x_train
    test = x_test

    inputs = x_train.shape[1]
    outputs = 9

    if args.training:
        red = RN(inputs, outputs)
        trainer = Sanger(red) if args.rule == "sanger" else Oja(red)
        trainer.fit_train(training, epochs=args.epochs, eta=args.eta)

        if args.output is not None:
            np.savetxt(args.output, fmt='%.6e')
    else:
        if args.rule == 'sanger':
            red = RN(inputs,outputs,w=np.loadtxt('networks/sanger.txt', dtype=float))
        else:
            red = RN(inputs,outputs,w=np.loadtxt('networks/oja.txt', dtype=float))

    results = []
    for x in training:
        y = red.eval(x).flatten()
        results.append(y)

    results_test = []
    for x in test:
        y = red.eval(x).flatten()
        results_test.append(y)

    results = np.array(results)
    results_test = np.array(results_test)
    graficar_componentes(results, y_train, results_test, y_test, args.rule, projection=1)
    graficar_componentes(results, y_train, results_test, y_test, args.rule, projection=2)
    graficar_componentes(results, y_train, results_test, y_test, args.rule, projection=3)

main()
