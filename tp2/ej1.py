#!/usr/bin/python3
import sys
import numpy as np
import pandas as pd
import argparse
import config
from sklearn.model_selection import train_test_split
import trained_networks
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
    parser.set_defaults(train=True)
    return parser.parse_args()


def main():

    args = parser_args()
    df = pd.read_csv(args.db)

    y = df[df.columns[0]]
    X = df[df.columns[1:]]

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=args.test_size, random_state=42)

    training = x_train.as_matrix()
    test = x_test.as_matrix()

    if args.train:
        inputs = x_train.shape[1]
        outputs = 9
        red = RN(inputs, outputs)
        trainer = Sanger(red) if args.rule == "sanger" else Oja(red)
        trainer.fit_train(training, epochs=args.epochs, eta=args.eta)

        if args.output is not None:
            with open(args.output, 'w') as f:
                f.write(str(red.w))
    else:
        if args.rule == 'sanger':
            red = trained_network.sanger_network
        else:
            red = trained_network.oja_network

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
    title = "Reduccion con " + ("Oja" if args.rule == 'oja' else 'Sanger')
    graficar_componentes(results, y_train, results_test, y_test, title)

main()
