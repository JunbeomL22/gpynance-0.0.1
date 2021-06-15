import unittest
from gpynance.utils import referencedate
from gpynance.parameters import dividend, curve
from gpynance.utils import data
#-
import QuantLib as ql
import numpy as np


class TestReference(unittest.TestCase):
    """
    To Check the change of reference date is updated to parameters, e.g., curve and dividend
    """
    def test_dividend(self):
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        times = np.array([1.0, 2.0, 3.0], dtype = 'float32')
        ratios= data.Data([0.01, 0.02, 0.01])
        div = dividend.Dividend(times, ratios, ref_date)
        x = [ref_date.date + ql.Period(i, ql.Years) for i in range(1, 4)]
        self.assertTrue(np.allclose(div(x), np.array([0.99, 0.9702, 0.96049803], dtype='float32')))

        # move the reference date
        ref_date.date += ql.Period("1D")
        self.assertTrue(np.allclose(div(x), np.array([1., 0.99, 0.9702], dtype='float32')))
        
