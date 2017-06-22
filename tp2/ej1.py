#!/usr/bin/python3
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from rn import RN
from trainer import Oja, Sanger, Trainer
from sklearn.decomposition import PCA
from graficar import graficar_componentes

def main():
    data = sys.argv[1]
    df = pd.read_csv(data)

    y = df[df.columns[0]]
    X = df[df.columns[1:]]

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=0.1, random_state=42)

    training = x_train.as_matrix()
    test = x_test.as_matrix()


    inputs = x_train.shape[1]
    outputs = 9
    red = RN(inputs, outputs)
    trainer = Sanger(red)

    # pca = PCA(n_components=9)
    # reduced = pca.fit_transform(x_train)
    #


    trainer.fit_train(training, epochs=500, eta=0.0001)

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
    graficar_componentes(results, y_train, results_test, y_test, "Reduccion con Oja")

main()
