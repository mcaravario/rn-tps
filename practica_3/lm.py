import abc
import numpy as np
import random

class LearningMethod:
    def __init__(self, neural_network):
        self.neural_network = neural_network

    def learn_one_epoch(self, training, *args, **kwargs):
        for x, y in training:
            self.learn_one_sample(x, y, *args, **kwargs)

    def learn_epochs(self, training, epochs=1, *args, **kwargs):
        for i in range(epochs):
            self.learn_one_epoch(training, *args, **kwargs)
            random.shuffle(training)

    @abc.abstractmethod
    def learn_one_sample(self, x, y, *args, **kwargs):
        return
