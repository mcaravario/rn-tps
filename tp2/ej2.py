#!/usr/bin/python3
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from rn import SOM
from trainer import SOMTrainer
import operator
from graficar import graficar_som

def main():
    data = sys.argv[1]
    df = pd.read_csv(data)

    y = df[df.columns[0]]
    X = df[df.columns[1:]]

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=0.1, random_state=42)

    training = x_train.as_matrix()

    inputs = x_train.as_matrix().shape[1]
    rows = 10
    cols = 10
    red = SOM(inputs, rows, cols)
    trainer = SOMTrainer(red)

    def get_grid(red, data, y_data):
        winning_table = [[{i: 0 for i in range(1,10)} for _ in range(cols)] for _ in range(rows)]

        for x, y in zip(data, y_data):
            i, j = red.winner(x)
            winning_table[i][j][y] += 1

        colors = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                colors[i][j] = max(winning_table[i][j].items(), key=operator.itemgetter(1))[0]
        return colors

    trainer.fit_train(training, eta0=0.01, sigma0=0.1, tao0=100, tao1=100, epochs=10)

    c = get_grid(red, training, y_train)
    print(c)
    graficar_som(c)



main()
