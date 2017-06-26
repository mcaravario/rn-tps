#!/usr/bin/python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

def graficar_componentes(matriz, y, matriz_test, y_test, rule, projection=1):

    c1 = matriz[:, 0:3]
    c2 = matriz[:, 3:6]
    c3 = matriz[:, 6:9]

    v1 = matriz_test[:, 0:3]
    v2 = matriz_test[:, 3:6]
    v3 = matriz_test[:, 6:9]

    POINT_SIZE = 10

    cmap = plt.get_cmap('jet', 9)

    y2 = list(map(lambda x: x, y))
    z2 = list(map(lambda x: x, y_test))

    fig = plt.figure()
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(c1[:,[0]], c1[:,[1]], c1[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=y2, marker='o')
    ax1.scatter(v1[:,[0]], v1[:,[1]], v1[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=z2, marker='^')

    ax1.set_title("Componentes 1 a 3")
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.set_title("Componentes 4 a 6")
    ax2.scatter(c2[:,[0]], c2[:,[1]], c2[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=y2, marker='o')
    ax2.scatter(v2[:,[0]], v2[:,[1]], v2[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=z2, marker='^')

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    ax3 = fig.add_subplot(133, projection='3d')

    ax3.set_title("Componentes 7 a 9")
    i = ax3.scatter(c3[:,[0]], c3[:,[1]], c3[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=y2,  marker='o')
    j = ax3.scatter(v3[:,[0]], v3[:,[1]], v3[:,[2]],vmin=1,vmax=9,cmap=cmap, s=POINT_SIZE, c=z2,  marker='^')
    cbar_ax3 = fig.add_axes()
    plt.colorbar(i, cax=cbar_ax3, extend='min')

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')

    # Figura 1 (Costado)
    if projection == 1:
        ax1.view_init(elev=10., azim=90)
        ax2.view_init(elev=10., azim=90)
        ax3.view_init(elev=10., azim=90)
    elif projection == 2: # Figura 2 (Top)
        ax1.view_init(elev=180., azim=90)
        ax2.view_init(elev=180., azim=90)
        ax3.view_init(elev=180., azim=90)
    else: # Figura 3 (Diagonal)
        ax1.view_init(elev=10., azim=135)
        ax2.view_init(elev=10., azim=135)
        ax3.view_init(elev=10., azim=135)

    plt.suptitle("Reduccion con {}".format(rule.capitalize()))
    plt.tight_layout()
    fig.savefig('componentes_{}_{}.png'.format(rule,projection))

def graficar_som(grilla_t, grilla_v, title, filename):
    fig = plt.figure(figsize=(16,7))

    cmap = plt.get_cmap('jet', 9)
    cmap.set_under('gray')

    ax1 = fig.add_subplot(121)
    ax1.set_title("Training")
    X1 = np.linspace(-grilla_t.shape[1]-1,0, grilla_t.shape[1]+1)
    Y1 = np.linspace(0,grilla_t.shape[0]+1, grilla_t.shape[0]+1)
    i1 = ax1.pcolor(X1,Y1,grilla_t,cmap=cmap,vmin=1, vmax=9, edgecolors='white')
    cbar_ax1 = fig.add_axes()
    plt.colorbar(i1, cax=cbar_ax1, extend='min')

    ax2 = fig.add_subplot(122)
    ax2.set_title("Validación")
    X2 = np.linspace(-grilla_v.shape[1]-1,0, grilla_v.shape[1]+1)
    Y2 = np.linspace(0,grilla_v.shape[0]+1, grilla_v.shape[0]+1)
    i2 = ax2.pcolor(X2,Y2,grilla_v,cmap=cmap,vmin=1, vmax=9, edgecolors='white')
    cbar_ax2 = fig.add_axes()
    plt.colorbar(i2, cax=cbar_ax2, extend='min')

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig('{}.png'.format(filename))
