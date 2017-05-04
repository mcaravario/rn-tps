import numpy as np

def get_normalization_function(training):
    xs, ys = zip(*training)
    avg_xs = np.mean(xs, axis=0)
    std_xs = np.std(xs, axis=0)
    return lambda x: ((x[0] - avg_xs)/std_xs, x[1])
