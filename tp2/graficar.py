#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

def graficar_componentes(matriz, y, matriz_test, y_test, tipo):

    c1 = matriz[:, 0:3]
    c2 = matriz[:, 3:6]
    c3 = matriz[:, 6:9]

    v1 = matriz_test[:, 0:3]
    v2 = matriz_test[:, 3:6]
    v3 = matriz_test[:, 6:9]

    POINT_SIZE = 10

    colors = cm.rainbow(np.linspace(0, 1, 9))
    y2 = list(map(lambda x: colors[x-1], y))
    z2 = list(map(lambda x: colors[x-1], y_test))

    fig = plt.figure()
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(c1[:,[0]], c1[:,[1]], c1[:,[2]], s=POINT_SIZE, facecolors=y2, marker='o')
    ax1.scatter(v1[:,[0]], v1[:,[1]], v1[:,[2]], s=POINT_SIZE, facecolors=z2, marker='^')

    ax1.set_title("Componentes 1 a 3")
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.set_title("Componentes 4 a 6")
    ax2.scatter(c2[:,[0]], c2[:,[1]], c2[:,[2]], s=POINT_SIZE, facecolors=y2, marker='o')
    ax2.scatter(v2[:,[0]], v2[:,[1]], v2[:,[2]], s=POINT_SIZE, facecolors=z2, marker='^')

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    ax3 = fig.add_subplot(133, projection='3d')

    ax3.set_title("Componentes 7 a 9")
    ax3.scatter(c3[:,[0]], c3[:,[1]], c3[:,[2]], s=POINT_SIZE, facecolors=y2, marker='o')
    ax3.scatter(v3[:,[0]], v3[:,[1]], v3[:,[2]], s=POINT_SIZE, facecolors=z2, marker='^')

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')

    # Figura 1 (Costado)
    # ax1.view_init(elev=10., azim=90)
    # ax2.view_init(elev=10., azim=90)
    # ax3.view_init(elev=10., azim=90)

    # Figura 2 (Top)
    # ax1.view_init(elev=180., azim=90)
    # ax2.view_init(elev=180., azim=90)
    # ax3.view_init(elev=180., azim=90)

    # Figura 3 (Diagonal)
    # ax1.view_init(elev=10., azim=135)
    # ax2.view_init(elev=10., azim=135)
    # ax3.view_init(elev=10., azim=135)

    plt.suptitle(tipo)
    plt.show()

def graficar_som(grilla):
    X = np.linspace(-grilla.shape[1]-1,0, grilla.shape[1]+1)
    Y = np.linspace(0,grilla.shape[0]+1, grilla.shape[0]+1)
    plt.pcolor(X,Y,grilla,vmin=1, vmax=9)
    plt.colorbar()
    plt.show()
