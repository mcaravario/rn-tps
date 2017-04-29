#!/bin/python3
import unittest
import numpy as np
import rn
import af
import lm

class TestRNMethods(unittest.TestCase):
    def test_weights(self):
        Ws = [np.array([[1, 2]])]
        n1 = rn.RN(gs=[lambda x: x], Ws=Ws)
        self.assertEqual(n1.weights(), Ws)
        Ws = [np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7, 8]])]
        n2 = rn.RN(gs=[lambda x: x, lambda x:x], Ws=Ws, biased=True)
        self.assertEqual(n2.weights(), Ws)

    def test_eval(self):
        nn_and = rn.RN(Ws=[np.array([[-0.75, 0.5, 0.5]])], gs=[af.sign()])
        self.assertEqual(nn_and.eval([1, 0, 0]), np.array([-1]))
        self.assertEqual(nn_and.eval([1, 0, 1]), np.array([-1]))
        self.assertEqual(nn_and.eval([1, 1, 0]), np.array([-1]))
        self.assertEqual(nn_and.eval([1, 1, 1]), np.array([1]))
        i = lambda x: x
        nn_2 = rn.RN(Ws=[np.array([[1, 2, 3],[4, 5, 6]]), np.array([[7, 8], [9, 10]])], gs=[i, i])
        # print(nn_2.eval([1, 0, 0]))
        self.assertTrue(np.array_equal(nn_2.eval([1,0,0]), np.array([39, 49])))
        self.assertTrue(np.array_equal(nn_2.eval([0,1,0]), np.array([54, 68])))
        self.assertTrue(np.array_equal(nn_2.eval([0,0,1]), np.array([69, 87])))

class TestLearnMethods(unittest.TestCase):
    def check_training(self, training, nn):
        for x, y in training:
            o = nn.eval(x).flatten().tolist()
            self.assertEqual(o, y)

    def test_AND(self):
        nn_and = rn.RN(ns=[3, 1], gs=[af.sign()], biased=True)
        l = lm.BackPropagation(nn_and)
        training = [([1,0,0],[-1]),
                    ([1,0,1],[-1]),
                    ([1,1,0],[-1]),
                    ([1,1,1],[1])]
        l.learn(training, epochs=10)
        self.check_training(training, nn_and)

    def test_XOR(self):
        nn_xor = rn.RN(ns=[2, 2, 1], gs=[af.sign(), af.sign()], biased=False)
        l = lm.BackPropagationOptimized(nn_xor)
        training = [([0,0],[-1]),
                    ([0,1],[1]),
                    ([1,0],[1]),
                    ([1,1],[-1])]
        l.learn(training, alpha=0.4, epochs=1000)
        self.check_training(training, nn_xor)

if __name__ == '__main__':
    unittest.main()
