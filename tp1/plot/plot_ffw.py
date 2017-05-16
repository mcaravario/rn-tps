import sys
import argparse
import pydot

def draw(dot, lista):
    nodes = dict()
    for l in range(len(lista)):
        for i in range(lista[l]):
            name = 'X_'+str(l)+'_'+str(i)
            node = pydot.Node(name,label="", color='blue', style="")
            nodes[name] = node
            dot.add_node(node)
            # dot.node('X_'+str(l)+'_'+str(i), "", color='blue')
            if l > 0:
                for j in range(lista[l-1]):
                    na = nodes['X_'+str(l)+'_'+str(i)]
                    nb = nodes['X_'+str(l-1)+'_'+str(j)]
                    edge = pydot.Edge(na, nb)
                    dot.add_edge(edge)

parser = argparse.ArgumentParser("Plotea red feed-foward")
parser.add_argument('input_units', metavar='U', type=int, nargs=1, help="Cantidad de entradas")
parser.add_argument('hidden_units', metavar='U', type=int, nargs='*', help="Cantidad de unidades ocultas")
parser.add_argument('output_units', metavar='U', type=int, nargs=1, help="Cantidad de salidas")
args = parser.parse_args()

dot = pydot.Dot(graph_type='graph')
architecture = args.input_units + args.hidden_units + args.output_units
print(architecture)
draw(dot, architecture)
dot.write_png("-".join(map(str,architecture))+".png")
