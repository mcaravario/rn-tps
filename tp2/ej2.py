#!/usr/bin/python3
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from rn import RN, SOM
from trainer import Oja, Sanger, SOMTrainer
import operator
from graficar import graficar_som
import trained_networks
import argparse
import config

def parser_args():
    parser = argparse.ArgumentParser(description='Entrena una red neuronal auto organizada')
    parser.add_argument('--db', type=str, help="Base de entrenamiento CSV", default=config.DB_TRAINING)
    parser.add_argument('-p', '--preprocess', help="Preprocesa la entrada usando Aprendizaje Hebiano", dest='preprocess', action='store_true')
    parser.add_argument('--no-preprocess', help="Usa la entrada original", dest='preprocess', action='store_false')
    parser.add_argument('-e', '--epochs', help="Cantidad de epocas", type=int, default=50)
    parser.add_argument('--test-size', help="Proporcion de test en la particion entrenamiento/test", type=float, default=0.3)
    parser.add_argument('-r', '--rows', help='Filas en la grilla SOM', type=int, default=10)
    parser.add_argument('-c', '--cols', help='Columnas en la grilla SOM', type=int, default=10)
    parser.add_argument('--eta0', help="Eta inicial", type=float, default=0.1)
    parser.add_argument('--sigma0', help="Sigma inicial", type=float, default=15)
    parser.add_argument('--tao0', help="Factor dilatacion del tiempo (eta)", type=float, default=2000)
    parser.add_argument('--tao1', help="Factor dilatacion del tiempo (sigma)", type=float, default=2000)
    parser.add_argument('--train', help="Modo entrenamiento", dest='training', action="store_true")
    parser.add_argument('--test', help="Testea la red ya entrenada", dest='training', action="store_false")
    parser.add_argument('--output', help="Salida con los pesos de la red", type=str)
    parser.add_argument('--normalize', help="Normaliza la entrada", dest='normalize', action='store_true')
    parser.add_argument('--no-normalize', help="No normaliza la entrada (defecto)", dest='normalize', action='store_false')
    parser.add_argument('--components', help="Cantidad de componentes en caso de preprocesado", type=int, default=9)
    parser.set_defaults(preprocess=False, train=True, normalize=False)
    return parser.parse_args()

def get_grid(red, data, y_data):
    winning_table = [[{i: 0 for i in range(0,10)} for _ in range(red.columns)] for _ in range(red.rows)]

    for x, y in zip(data, y_data):
        i, j = red.winner(x)
        winning_table[i][j][y] += 1

    colors = np.zeros((red.rows, red.columns))
    for i in range(red.rows):
        for j in range(red.columns):
            colors[i][j] = max(winning_table[i][j].items(), key=operator.itemgetter(1))[0]
    return colors



def main():
    args = parser_args()
    df = pd.read_csv(args.db, header=None)

    y = df[df.columns[0]]
    X = df[df.columns[1:]].as_matrix()

    if args.normalize:
        X = StandardScaler().fit_transform(X)

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=args.test_size, random_state=42)

    training = x_train
    tests = x_test

    if args.preprocess:
        inputs = x_train.shape[1]
        outputs = args.components
        red = RN(inputs, outputs)
        trainer = Sanger(red)

        trainer.fit_train(training, epochs=500, eta=0.0001)

        results = []
        for x in training:
            y = red.eval(x).flatten()
            results.append(y)

        results_test = []
        for x in tests:
            y = red.eval(x).flatten()
            results_test.append(y)

        training = np.array(results)
        tests = np.array(results_test)
        print("Preprocess finished")


    inputs = training.shape[1]
    if args.train:
        red = SOM(inputs, args.rows, args.cols)
        trainer = SOMTrainer(red)
        trainer.fit_train(training, eta0=args.eta0, sigma0=args.sigma0, tao0=args.tao0, tao1=args.tao1, epochs=args.epochs)

        if args.output is not None:
            with open(args.output, 'w') as f:
                f.write(str(red.w))
    else:
        red = trained_networks.som_network

    c = get_grid(red, training, y_train)
    c2 = get_grid(red, tests, y_test)

    def get_filename(grilla, pre):
        return 'som_{}_{}{}'.format(grilla.shape[0], grilla.shape[1],
                                    '_{}_preprocess'.format(args.components) if pre else '')

    graficar_som(c, c2, "Activaciones SOM", get_filename(c, args.preprocess))

main()
