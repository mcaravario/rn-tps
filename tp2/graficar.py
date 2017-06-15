#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

def graficar_componentes(matriz, y):

    c1 = matriz[:, 0:3]
    c2 = matriz[:, 3:6]
    c3 = matriz[:, 6:9]

    colors = cm.rainbow(np.linspace(0, 1, 9))
    y2 = list(map(lambda x: colors[x-1], y))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(c1[:,[0]], c1[:,[1]], c1[:,[2]], c=y2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


    plt.show()
