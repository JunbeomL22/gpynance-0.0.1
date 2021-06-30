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

        path1 = path.SinglePath(dtg, path_data[:, 0, :], past1, name = "the first path in path_test", xp = np)
        path2 = path.SinglePath(dtg, path_data[:, 1, :], past2, name = "the second path in path_test", xp = np)

        path_test = path.MultiPath(dtg, [path1, path2], name = "multi path in path_test")

        d0 = ql.Date(6, 1, 2021)
        d1 = ql.Date(1, 1, 2021)
        d2 = ql.Date(31, 12, 2020)
        d3 = ql.Date(30, 12, 2020)

        check0 = path_test(d0)
        check1 = path_test(d1)
        check2 = path_test(d2)

        self.assertTrue(np.allclose(check0[0], np.array([[ 2.], [14.]], dtype='float32')))
        self.assertTrue(np.allclose(check0[1], np.array([[ 8.], [20.]], dtype='float32')))
        self.assertTrue(np.allclose(check1[0], np.array([[ 0.], [12.]], dtype='float32')))
        self.assertTrue(np.allclose(check1[1], np.array([[ 6.], [18.]], dtype='float32')))

        # test slicing
        foo0 = path_test(ql.Date(5, 1, 2021), num=3)[0]
        foo1 = path_test(ql.Date(5, 1, 2021), num=3)[1]
        foo_res0=np.array([[-2.,  0.,  1.], [-2.,  12.,  13.]])
        foo_res1=np.array([[-5., 6., 7.],  [-5., 18., 19.]])
        
        self.assertTrue(np.allclose(foo0, foo_res0))
        self.assertTrue(np.allclose(foo1, foo_res1))

    def test_single_path(self):
        ref = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
        dtg = datetimegrid.DateTimeGrid(ref, ref.date + ql.Period("1W"))
        path_data = np.array(np.arange(24).reshape(4, 6), dtype='float32')
        past= {ql.Date(1, 1, 2021): -1.0, ql.Date(30, 12, 2020): -2.0, ql.Date(29, 12, 2020): -3.0}

        singlepath = path.SinglePath(dtg, path_data, past, name = "test")

        d0 = ql.Date(6, 1, 2021)
        d1 = ql.Date(1, 1, 2021)
        d2 = ql.Date(31, 12, 2020)
        d3 = ql.Date(30, 12, 2020)

        check0 = singlepath(d0, 5)
        self.assertEqual(check0.tolist(), [[-3., -2.,  0.,  1.,  2.], [-3., -2.,  6.,  7.,  8.], [-3., -2., 12., 13., 14.], [-3., -2., 18., 19., 20.]])

        
