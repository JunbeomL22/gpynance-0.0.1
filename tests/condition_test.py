import unittest
from gpynance.products import condition
# -
import numpy as np

class TestCondition(unittest.TestCase):
    def test_lowerbarrier(self):
        lbar = condition.LowerBarrier(0.8)
        x = np.linspace(0.0, 2.0, 21)
        res = lbar(x)
        self.assertTrue(all(res[:8] == False))
        self.assertTrue(all(res[9:] == True))

    def test_upperbarrier(self):
        ubar = condition.UpperBarrier(1.2)
        x = np.linspace(0.0, 2.0, 21)
        res = ubar(x)
        self.assertTrue(all(res[:11] == True))
        self.assertTrue(all(res[12:] == False))
        
    def test_lower_path_barrier(self):
        lp_bar = condition.LowerPathBarrier(0.6)
        x = np.linspace(0.0, 2.0, 20).reshape(2, 10)
        res = lp_bar(x)
        self.assertEqual(res.tolist(), [False, True])

    def test_upper_path_barrier(self):
        up_bar = condition.UpperPathBarrier(1.2)
        x = np.linspace(0.0, 2.0, 20).reshape(2, 10)
        res = up_bar(x)
        self.assertEqual(res.tolist(), [True, False])
