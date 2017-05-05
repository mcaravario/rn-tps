import numpy as np

def get_normalization_function(training):
    xs, ys = zip(*training)
    avg_xs = np.mean(xs, axis=0)
    std_xs = np.std(xs, axis=0)
    def t(x):
        r = [None for i in range(len(x[0]))]
        for i in range(len(x[0])):
            if std_xs[i] != 0:
                r[i] = (x[0][i] - avg_xs[i])/std_xs[i]
            else:
                r[i] = 0
        return (r, x[1])
    return t
