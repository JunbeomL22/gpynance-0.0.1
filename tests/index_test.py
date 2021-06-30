import unittest
# - 
from gpynance.parameters import index, curve
from gpynance.utils import data, referencedate
# -
import numpy as np
import QuantLib as ql

class TestIndex(unittest.TestCase):
    def test_dividend_ref_date(self):
        ref_date = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
        times = [1.0]
        rates = data.Data([0.02])
        yts = curve.ZeroCurve(times, rates, ref_date)

        past = {ql.Date(30, 12, 2020): 0.01, ql.Date(29, 12, 2020): 0.1}
        dc = ql.Actual365Fixed()

        cd = index.CD91(yts, dc, past)

        self.assertTrue(np.isclose(cd.fixing(ref_date.date), 0.019899565814920226))
        d = ql.Date(1, 6, 2021)
        self.assertTrue(np.isclose(cd.fixing(d), 0.019899565814920226))
        d = ql.Date(30, 12, 2020)
        self.assertTrue(np.isclose(cd.fixing(d), 0.01))
        d = ql.Date(29, 12, 2020)
        self.assertTrue(np.isclose(cd.fixing(d), 0.1))
        d = ql.Date(31, 12, 2020)
        self.assertTrue(np.isclose(cd.fixing(d), 0.019899565814920226))
        
