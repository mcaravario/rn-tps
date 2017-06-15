#!/usr/bin/python3
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from rn import RN
from trainer import Oja, Sanger, Trainer

def main():
    data = sys.argv[1]
    df = pd.read_csv(data)

    y = df[df.columns[0]]
    X = df[df.columns[1:]]

    x_train, x_test, y_train, y_test =  train_test_split(X, y, test_size=0.1, random_state=42)


    inputs = x_train.shape[1]
    outputs = 9
    red = RN(inputs, outputs)
    trainer = Oja(red)

    for x in x_train.as_matrix():
        trainer.fit(x, 0.0001)

    # print(red.w)

main()
