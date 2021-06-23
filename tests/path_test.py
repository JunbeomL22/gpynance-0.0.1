import unittest
from gpynance.engines.montecarlo import path
from gpynance.utils import datetimegrid, referencedate
#-
import QuantLib as ql
import numpy as np

class TestPath(unittest.TestCase):
    def test_path_slicing(self):
        ref = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
        dtg = datetimegrid.DateTimeGrid(ref, ref.date + ql.Period("1W"))
        path_data = np.array(np.arange(24).reshape(2, 2, 6), dtype='float32')
        past1= {ql.Date(1, 1, 2021): -1.0, ql.Date(30, 12, 2020): -2.0, ql.Date(29, 12, 2020): -3.0}
        past2= {ql.Date(1, 1, 2021): -4.0, ql.Date(30, 12, 2020): -5.0, ql.Date(29, 12, 2020): -6.0}
        past = [past1, past2]
        path_test = path.Path(dtg, path_data, past, name = "test")

        d0 = ql.Date(6, 1, 2021)
        d1 = ql.Date(1, 1, 2021)
        d2 = ql.Date(31, 12, 2020)
        d3 = ql.Date(30, 12, 2020)

        check0 = path_test(d0)
        check1 = path_test(d1)
        check2 = path_test(d2)

        self.assertEqual(check0.tolist(),  [[[ 2.],[ 8.]], [[14.], [20.]]])
        self.assertEqual(check1.tolist(),  [[[ -1.],[ -4.]], [[-1.], [-4.]]])
        self.assertEqual(check2.tolist(),  [[[ 0.],[ 6.]], [[0.], [6.]]])

        # test slicing
        foo = path_test(ql.Date(5, 1, 2021), num=3).tolist()
        foo_res=[[[-2.,  0.,  1.], [-5.,  6.,  7.]],  [[-2., 12., 13.],  [-5., 18., 19.]]]
        self.assertEqual(foo, foo_res)

