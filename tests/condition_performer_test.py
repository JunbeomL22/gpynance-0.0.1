import unittest
from gpynance.products import performer, condition
# -
import numpy as np

class TestConditionPerformer(unittest.TestCase):
    def test_conditions_on_worst_performer(self):
        m = np.empty((2, 3, 3))
        m[0] = np.array([[0.5, 1.0, 2.0], [1.0, 2.0, 0.5], [0.5, 0.7, 2.0]])
        m[1] = np.array([[1.5, 1.0, 2.0], [1.0, 2.0, 0.9], [3.5, -0.5, 1.0]])
        
        perf = performer.WorstPerformer()
        lbar = condition.LowerBarrier(0.8)
        lpbar= condition.LowerPathBarrier(0.4)
        
        self.assertEqual(lbar(perf(m[:, :, 0])).tolist(), [False, True])
        self.assertEqual(lbar(perf(m[:, :, 1])).tolist(), [False, False])
        self.assertEqual(lbar(perf(m[:, :, 2])).tolist(), [False, True])

        self.assertEqual(lpbar(perf(m)).tolist(), [True, False])
