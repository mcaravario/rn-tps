#!/usr/bin/python3

from tp1 import rn
from tp1 import af

# TODO: Poner mejor Red
red = RN(ns=[10,20,1], gs=[af.sigmoid(), af.sign()])
# TODO: Poner normalización de la mejor red
avg_std = (0.0, 1.0, 0.0, 1.0)
