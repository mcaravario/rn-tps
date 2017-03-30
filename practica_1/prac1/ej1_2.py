import numpy as np
from matplotlib import pyplot as mpl

INTERVAL = (-2, 2)
SAMPLES = 100

fs = [lambda x: 1.0 / (1 + np.exp(-x)),     # 1.
      lambda x: np.tanh(x),                 # 2.
      lambda x: np.sign(x),                 # 3.
      lambda x: fs[0](x) * (1 - fs[0](x)),  # 4.
      lambda x: 1 - fs[1](x)**2]            # 5.

def derivate(f, diff=0.0001):
	"""Calcula la funcion derivada de @f."""
	def fprime(x):
		return (f(x+diff)-f(x))/diff
	return fprime

def plot_functions(f1, f2, interval=INTERVAL, samples=SAMPLES):
	X = np.linspace(interval[0], interval[1], samples)
	Y1 = [f1(x) for x in X]
	Y2 = [f2(x) for x in X]
	mpl.plot(X,Y1,X,Y2)
	mpl.show()

def plot_w_derivate(f, interval=INTERVAL, samples=SAMPLES):
	plot_functions(f, derivate(f), interval, samples)

for f in fs:
	plot_w_derivate(f)
