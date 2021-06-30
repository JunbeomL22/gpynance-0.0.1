import unittest
from gpynance.products import condition
# -
import numpy as np

class TestCondition(unittest.TestCase):
    def test_conditions_on_worst_performer(self):
        m = np.empty((2, 3, 3))
        m[0] = np.array([[0.5, 1.0, 2.0], [1.0, 2.0, 0.5], [0.5, 0.7, 2.0]])
        m[1] = np.array([[1.5, 1.0, 2.0], [1.0, 2.0, 0.9], [3.5, -0.5, 1.0]])
        
        lbar = condition.WorstLowerBarrier(base_price=[1.0, 1.0, 1.0], barrier_ratio = 0.8)
        self.assertEqual(lbar(m[:, :, 0]).tolist(), [False, True, False])
        self.assertEqual(lbar(m[:, :, 1]).tolist(), [True, True, False])

        
        lpbar= condition.PathWorstLowerBarrier(base_price=[1.0, 1.0, 1.0], barrier_ratio = 0.4)
        self.assertEqual(lpbar(m).tolist(), [True, True, False])
        lpbar= condition.PathWorstLowerBarrier(base_price=[1.0, 1.0, 1.0], barrier_ratio = 0.6)
        self.assertEqual(lpbar(m).tolist(), [False, False, False])
        lpbar= condition.PathWorstLowerBarrier(base_price=[1.0, 1.0, 1.0], barrier_ratio = -0.6)
        self.assertEqual(lpbar(m).tolist(), [True, True, True])
