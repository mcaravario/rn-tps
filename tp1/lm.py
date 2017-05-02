import abc
import numpy as np
import random
import math
from enum import Enum

# from logger import log

ETA = 0.3
ALPHA = 0.7
DEBUG = False

def print_args(name):
    def wrapper(funct):
        def new_funct(*args, **kwargs):
            if DEBUG:
                print("----------------------------------")
                print("Llamando a {} con parametros:".format(name))
                print("Con nombre: {}".format(",".join(map(str,kwargs.items()))))
            return funct(*args, **kwargs)
        return new_funct
    return wrapper


class TrainMode(Enum):
    STOCHASTIC = 1
    BATCH = 2
    MINI_BATCH = 3

class LearningMethod:
    def __init__(self, neural_network):
        """ Constructor del Método de aprendizaje
        neural_network: Red neuronal que va a aprender
        """

        self.neural_network = neural_network

    @print_args('learn_one_epoch_learning_method')
    def learn_one_epoch(self, training, *args, **kwargs):
        """ Aprende del conjunto de training una sola epoca"""
        nn = self.neural_network

        if 'training_mode' in kwargs:
            training_mode = kwargs['training_mode']
            del kwargs['training_mode']
        else:
            training_mode = TrainMode.BATCH

        if 'batch_size' in kwargs:
            batch_size = kwargs['batch_size']
            del kwargs['batch_size']
        else:
            batch_size = 2

        if training_mode is TrainMode.STOCHASTIC:
            batch_size = 1
        elif training_mode is TrainMode.BATCH:
            batch_size = len(training)

        r = len(training) % batch_size
        n = len(training) // batch_size

        if r > 0:
            n += 1

        for i in range(0, n):
            suma_delta_Ws = [np.zeros(W.shape, dtype=np.float64) for W in nn.Ws]

            m = r if i == n-1 and r > 0 else batch_size

            for j in range(0, m):
                x, y = training[i*batch_size + j]
                delta_Ws = self.get_delta_Ws(x, y, *args, **kwargs)
                for k in range(nn.nr_layers):
                    suma_delta_Ws[k] += delta_Ws[k]
            for k in range(nn.nr_layers):
                nn.Ws[k] += suma_delta_Ws[k] / float(m)

        # Calcula error de la epoca
        return nn.error_training(training)



    @print_args('learn_learning_method')
    def learn(self, training, epochs=1, *args, **kwargs):
        for epoch in range(epochs):
            error = self.learn_one_epoch(training, *args, **kwargs)
            yield epoch, error
            random.shuffle(training)

    @abc.abstractmethod
    def get_delta_Ws(self, x, y, *args, **kwargs):
        """ Aprende una sola muestra con su solucion"""
        return

class BackPropagation(LearningMethod):
    def __init__(self, neural_network):
        super(BackPropagation, self).__init__(neural_network)

    @print_args('get_delta_Ws')
    def get_delta_Ws(self, x, y, eta=ETA):
        vs = self.forward(x)
        return self.backward(vs, y, eta)

    def forward(self, x):
        """ Paso Forward del Backpropagation """
        vs = []
        nn = self.neural_network

        y = list(x)
        if not nn.biased:
            y.insert(0, 1.0)

        y = np.array(y).reshape((nn.Ws[0].shape[1], 1))

        vs.append((None, y))
        for W, g in zip(nn.Ws, nn.gs):
            h = np.dot(W, y)
            y = g(h)
            vs.append((h,y))
        return vs

    @print_args('backward')
    def backward(self, vs, y, eta=ETA):
       """ Paso Backward del Backpropagation """
       ######################################################
       ##        W en R^(salidas * entradas)               ##
       ##--------------------------------------------------##
       ##                                                  ##
       ##  W_{i,j} = el peso de la entrada j a la salida i ##
       #####################################################
       nn = self.neural_network
       delta_Ws = [None for i in range(self.neural_network.nr_layers)]

       last_layer = -1
       # W es la matriz de la ultima capa
       W = nn.Ws[last_layer]
       # La ultima capa
       assert(len(y) == W.shape[0])
       # interpretamos y como un vector columna
       y = np.array(y).reshape((W.shape[0], 1))

       delta = np.zeros((W.shape[0], 1))
       g = nn.gs[last_layer]
       h, v = vs[last_layer]

       delta = g.dif(h) * (y - v) # multiplicacion elemento a elemento
       delta_W = eta * delta * vs[last_layer-1][1].T
       prev_W = W
       delta_Ws[last_layer] = delta_W

       for m in range(nn.nr_layers-2, -1, -1):

           g = nn.gs[m]
           h, v = vs[m+1]

           # s = np.zeros(h.shape)
           s = np.dot(prev_W.T, delta)
           # Multiplicacion elemento a elemento
           delta = g.dif(h) * s
           delta_W = eta * (delta * vs[m][1].T)
           prev_W = nn.Ws[m]
           delta_Ws[m] = delta_W
       return delta_Ws

class BackPropagationOptimized(BackPropagation):
    def __init__(self, neural_network):
        super(BackPropagationOptimized, self).__init__(neural_network)
        self.delta_W_prev = [np.zeros(W.shape) for W in self.neural_network.Ws]

    @print_args('learn_adaptative_optimiezed')
    def learn_adaptative(self, training, epochs=1, eta=ETA, a=1, b=2, *args, **kwargs):
        last_error = None
        for epoch in range(epochs):
            error = self.learn_one_epoch(training, eta, *args, **kwargs)
            yield epoch, error
            if epoch > 0:
                delta_error = error-last_error
                delta_eta = 0
                if delta_error > 0.0:
                    delta_eta = -b * eta
                elif delta_error < 0.0:
                    delta_eta = a

                eta += delta_eta

            last_error = error
            random.shuffle(training)

    @print_args("get_delta_Ws_optimized")
    def get_delta_Ws(self, x, y, eta=ETA, alpha=ALPHA):
        vs = self.forward(x)
        for l, delta_W in enumerate(self.backward(vs, y, eta)):
            delta_W = delta_W + alpha * self.delta_W_prev[l]
            self.delta_W_prev[l] += delta_W
        return self.delta_W_prev
