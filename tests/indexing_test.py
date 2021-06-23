import unittest
from gpynance.processes import process
from gpynance.utils import indexing
# -
import numpy as np

class TestIndexing(unittest.TestCase):
    def test_indexing(self):
        procs = process.Processes(procs = [process.Process1D(0.0), process.Process2D(0.0), process.Process1D(0.0)])
        cnt, idx = indexing.slicing_brownianmotion(procs)

        foo = np.arange(cnt).tolist()
        self.assertEqual(cnt, 4)
        self.assertEqual(foo[idx[0]], [0])
        self.assertEqual(foo[idx[1]], [1, 2])
        self.assertEqual(foo[idx[2]], [3])

        
        
