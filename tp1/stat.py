import numpy as np

def norm_training_funct(training):
    xs, ys = zip(*training)
    avg_xs = np.mean(xs)
    std_xs = np.std(xs)
    return lambda x: ((x[0] - avg_xs)/std_xs, x[1])
