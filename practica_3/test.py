#!/bin/python3
import unittest
import numpy as np
import rn
import af

class TestRNMethods(unittest.TestCase):
    def test_weights(self):
        Ws = [np.array([[1, 2]])]
        n1 = rn.RN(gs=[lambda x: x], Ws=Ws)
        self.assertEqual(n1.weights(), Ws)
        Ws = [np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7, 8]])]
        n2 = rn.RN(gs=[lambda x: x, lambda x:x], Ws=Ws)
        self.assertEqual(n2.weights(), Ws)

    def test_eval(self):
        nn_and = rn.RN(Ws=[np.array([[-0.75, 0.5, 0.5]])], gs=[af.sign()])
        self.assertEqual(nn_and.eval([1, 0, 0]), np.array([[-1]]))
        self.assertEqual(nn_and.eval([1, 0, 1]), np.array([[-1]]))
        self.assertEqual(nn_and.eval([1, 1, 0]), np.array([[-1]]))
        self.assertEqual(nn_and.eval([1, 1, 1]), np.array([[1]]))
        i = lambda x: x
        nn_2 = rn.RN(Ws=[np.array([[1, 2, 3],[4, 5, 6]]), np.array([[7, 8], [9, 10]])], gs=[i, i])
        # print(nn_2.eval([1, 0, 0]))
        self.assertTrue(np.array_equal(nn_2.eval([1,0,0]), np.array([[39], [49]])))
        self.assertTrue(np.array_equal(nn_2.eval([0,1,0]), np.array([[54], [68]])))
        self.assertTrue(np.array_equal(nn_2.eval([0,0,1]), np.array([[69], [87]])))

if __name__ == '__main__':
    unittest.main()
