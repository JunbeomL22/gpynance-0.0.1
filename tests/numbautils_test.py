import unittest
from gpynance.utils import numbautils
# -
import numpy as np

class TestNumbautils(unittest.TestCase):
    def test_numbautils_sortedindexf4(self):
        x = np.linspace(0.0, 20.0, 21, dtype = 'float32')
        n = x.shape[0]
        
        func = numbautils.sortedindexf4

        idx, ratio = func(x, 1.2)
        val = x[idx]*ratio +x[min(idx+1, n)] * (1.-ratio)
        self.assertEqual(idx, 1)
        self.assertTrue(np.isclose(val, 1.2))

        idx, ratio = func(x, -1.0)
        val = x[idx]*ratio +x[min(idx+1, n)] * (1.-ratio)
        self.assertEqual(idx, 0)
        self.assertTrue(np.isclose(val, 0.0))

        idx, ratio = func(x, 22.0)
        val = x[idx]*ratio +x[min(idx+1, n)] * (1.-ratio)
        self.assertEqual(idx, -1)
        self.assertTrue(np.isclose(val, 20.0))
