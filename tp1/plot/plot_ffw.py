import sys
import argparse
from graphviz import Graph

def draw(dot, lista):
    for l in range(len(lista)):
        for i in range(lista[l]):
            dot.node('X_'+str(l)+'_'+str(i), "", color='blue')
            if l > 0:
                for j in range(lista[l-1]):
                    dot.edge('X_'+str(l)+'_'+str(i), 'X_'+str(l-1)+'_'+str(j))

parser = argparse.ArgumentParser("Plotea red feed-foward")
parser.add_argument('input_units', metavar='U', type=int, nargs=1, help="Cantidad de entradas")
parser.add_argument('hidden_units', metavar='U', type=int, nargs='*', help="Cantidad de unidades ocultas")
parser.add_argument('output_units', metavar='U', type=int, nargs=1, help="Cantidad de salidas")
args = parser.parse_args()

dot = Graph(comment='Graph')
architecture = args.input_units + args.hidden_units + args.output_units
print(architecture)
draw(dot, architecture)
dot.render("-".join(map(str,architecture))+".svg", view=True)
