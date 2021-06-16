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
        """
        the reference date behavior for dividend
        """
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dates = [ref_date.date + ql.Period(f"{i}Y") for i in range(1, 4)]
        ratios= data.Data([0.01, 0.02, 0.01])
        div = dividend.Dividend(dates, ratios, ref_date)
        self.assertTrue(np.allclose(div(dates), np.array([0.99, 0.9702, 0.96049803], dtype='float32')))

        # move the reference date
        ref_date.date += ql.Period("1D")
        self.assertTrue(np.allclose(div(dates), np.array([1., 0.99, 0.9702], dtype='float32')))
        
