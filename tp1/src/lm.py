import abc
import numpy as np
import random

ETA = 0.3
ALPHA = 0.7

def preprocess_normalize(training):
    xs, ys = zip(*training)
    avg_xs = numpy.mean(xs)
    std_xs = numpy.std(xs)
    xs_p = map(lambda x: (x-agv_xs)/std_xs, xs)
    return avg_xs, std_xs, list(zip(xs_p, ys))

class LearningMethod:
    def __init__(self, neural_network):
        """ Constructor del Método de aprendizaje
        neural_network: Red neuronal que va a aprender
        """

        self.neural_network = neural_network

    def learn_one_epoch(self, training, *args, **kwargs):
        """ Aprende del conjunto de training una sola epoca"""
        for x, y in training:
            self.learn_one_sample(x, y, *args, **kwargs)

        # Calcula error de la epoca
        error = 0.0
        for x,y in training:
            error += self.neural_network.get_error(x,y)
        return error/len(training)



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
    def learn_one_sample(self, x, y, *args, **kwargs):
        """ Aprende una sola muestra con su solucion"""
        return

class BackPropagation(LearningMethod):
    def __init__(self, neural_network):
        super(BackPropagation, self).__init__(neural_network)

    def learn_one_sample(self, x, y, eta=ETA):
        vs = self.forward(x)
        for l, delta_W in self.backward(vs, y, eta):
            self.neural_network.Ws[l] += delta_W

    def forward(self, x):
        """ Paso Forward del Backpropagation """
        vs = []
        nn = self.neural_network
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
       prev_W = np.copy(W)
       yield last_layer, delta_W

       for m in range(len(nn.Ws)-2, -1, -1):

           g = nn.gs[m]
           h, v = vs[m+1]

           # s = np.zeros(h.shape)
           s = np.dot(prev_W.T, delta)
           # Multiplicacion elemento a elemento
           delta = g.dif(h) * s
           delta_W = eta * (delta * vs[m][1].T)
           prev_W = np.copy(nn.Ws[m])
           yield m, delta_W

class BackPropagationMomentum(BackPropagation):
    def __init__(self, neural_network):
        super(BackPropagationMomentum, self).__init__(neural_network)
        self.delta_W_prev = [np.zeros(W.shape) for W in self.neural_network.Ws]

    def learn_one_sample(self, x, y, eta=ETA, alpha=ALPHA):
        vs = self.forward(x)
        #self.delta_W_prev
        for l, delta_W in self.backward(vs, y, eta):
            delta_W = delta_W + alpha * self.delta_W_prev[l]
            self.delta_W_prev[l] = delta_W
            self.neural_network.Ws[l] += delta_W
