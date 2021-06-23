import unittest
from gpynance.products import performer
# -
import numpy as np

class TestPerformer(unittest.TestCase):
    def test_all_performers(self):
        m = np.empty((2, 2, 3))
        m[0] = np.array([[0.5, -1.0, 2.0], [1.0, 2.0, -0.3] ])
        m[1] = np.array([[1.5, 1.0, -2.0], [1.0, -2.0, -0.3] ])
        perf = performer.WorstPerformer()
        res_path = perf(m)
        self.assertTrue(np.allclose(res_path, np.array([[ 0.5, -1. , -0.3], [ 1. , -2. , -2. ]])))

        perf = performer.BestPerformer()
        res_path = perf(m)
        self.assertTrue(np.allclose(res_path, np.array([[ 1. ,  2. ,  2. ], [ 1.5,  1. , -0.3]])))

        perf = performer.AveragePerformer()
        res_path = perf(m)
        self.assertTrue(np.allclose(res_path, np.array([[ 0.75,  0.5 ,  0.85], [ 1.25, -0.5 , -1.15]])))
