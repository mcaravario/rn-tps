import abc
import numpy as np
import random
import math
from enum import Enum

from logger import log

ETA = 0.3
ALPHA = 0.7

class TrainMode(Enum):
    STOCHASTIC = 1
    BATCH = 2
    MINI_BATCH = 3

def preprocess_normalize(training):
    xs, ys = zip(*training)
    avg_xs = np.mean(xs)
    std_xs = np.std(xs)
    xs_p = map(lambda x: (x-avg_xs)/std_xs, xs)
    return avg_xs, std_xs, list(zip(xs_p, ys))

class LearningMethod:
    def __init__(self, neural_network):
        """ Constructor del Método de aprendizaje
        neural_network: Red neuronal que va a aprender
        """

        self.neural_network = neural_network

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

        n = math.ceil(len(training) / batch_size)
        for i in range(0, n):
            suma_delta_Ws = [np.zeros(W.shape) for W in nn.Ws]
            if len(training) % batch_size != 0 and i == n-1:
                m = len(training) - batch_size * n
            else:
                m = batch_size
            for j in range(0, m):
                x, y = training[i*batch_size + j]
                delta_Ws = self.get_delta_Ws(x, y, *args, **kwargs)
                for k in range(nn.nr_layers):
                    suma_delta_Ws[k] += delta_Ws[k]
            for k in range(nn.nr_layers):
                nn.Ws[k] += suma_delta_Ws[k] * 1.0 / float(batch_size)

        # Calcula error de la epoca
        error = 0.0
        for x,y in training:
            error += self.neural_network.get_error(x,y)
        return error / len(training)



    def learn(self, training, epochs=1, *args, **kwargs):
        """ Aprende tantas epocas del conjunto training como se le
        indique en epochs"""
        preprocess =  kwargs.get('preprocess') or False

        if preprocess:
            _, _, training = preprocess_normalize(training)

        list_errors = [None for i in range(epochs)]
        for epoch in range(epochs):
            error = self.learn_one_epoch(training, *args, **kwargs)
            list_errors[epoch] = error
            random.shuffle(training)
        return list_errors

    @abc.abstractmethod
    def get_delta_Ws(self, x, y, *args, **kwargs):
        """ Aprende una sola muestra con su solucion"""
        return

class BackPropagation(LearningMethod):
    def __init__(self, neural_network):
        super(BackPropagation, self).__init__(neural_network)

    def get_delta_Ws(self, x, y, eta=ETA):
        vs = self.forward(x)
        return self.backward(vs, y, eta)

    def forward(self, x):
        """ Paso Forward del Backpropagation """
        vs = []
        nn = self.neural_network

        x = list(x)
        if not nn.biased:
            x.insert(0, 1.0)

        x = np.array(x).reshape((nn.Ws[0].shape[1], 1))

        vs.append((None, x))
        for W, g in zip(nn.Ws, nn.gs):
            y = np.dot(W, x)
            x = g(y)
            vs.append((y,x))
        return vs

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

    def learn_adaptative(self, training, epochs=1, eta=ETA, a=1, b=2, *args, **kwargs):
        preprocess =  kwargs.get('preprocess') or False

        if preprocess:
            _, _, training = preprocess_normalize(training)

        list_errors = []
        for epoch in range(epochs):
            error = self.learn_one_epoch(training, eta, *args, **kwargs)
            if epoch > 0:
                delta_error = error-list_errors[-1]
                delta_eta = 0
                if delta_error > 0.0:
                    delta_eta = -b * eta
                elif delta_error < 0.0:
                    delta_eta = a

                eta += delta_eta

            list_errors.append(error)
            random.shuffle(training)
        return list_errors

    def learn_one_sample(self, x, y, eta=ETA, alpha=ALPHA):
        vs = self.forward(x)
        #self.delta_W_prev
        for l, delta_W in self.backward(vs, y, eta):
            delta_W = delta_W + alpha * self.delta_W_prev[l]
            self.delta_W_prev[l] = delta_W
            self.neural_network.Ws[l] += delta_W
