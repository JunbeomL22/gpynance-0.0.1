import unittest
from gpynance.parameters import dividend
from gpynance.utils import referencedate
from gpynance.utils import data
from gpynance.utils import utils
#-
import numpy as np
import QuantLib as ql

class TestDividend(unittest.TestCase):
    def test_dividend_ref_date(self):
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dates = [ref_date.date + ql.Period(f"{i}D") for i in range(1, 4)]
        w = utils.WhatTimeIs(ref_date, dtype='float64')
        x = w([ref_date.date, *dates])

        ratios = data.Data([0.01, 0.02, 0.03])
        div = dividend.Dividend(dates, ratios, ref_date = ref_date, xp = np, dtype = 'float64')
        self.assertTrue(np.allclose(div(x), np.array([1.0, 0.99, 0.9702, 0.941094])))
        
        # check the case when dividend is paid tommorow
        one_day = ql.Period("1D")
        ref_date +=one_day # ref_date already notifies dividend. Notification is implemented in __iadd__
        self.assertTrue(np.allclose(div(x), np.array([0.99, 0.9702, 0.941094, 0.941094])))

        # move it back
        ref_date -=one_day 
        self.assertTrue(np.allclose(div(x), np.array([1.0, 0.99, 0.9702, 0.941094])))

    def test_dividend_data(self):
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dates = [ref_date.date + ql.Period(f"{i}D") for i in range(1, 4)]
        w = utils.WhatTimeIs(ref_date, dtype='float64')
        x = w([ref_date.date, *dates])

        ratios = data.Data([0.01, 0.02, 0.03])
        div = dividend.Dividend(dates, ratios, ref_date = ref_date, xp = np, dtype = 'float64')
        self.assertTrue(np.allclose(div(x), np.array([1.0, 0.99, 0.9702, 0.941094])))

        # purturb the data
        ratios += 0.01
        self.assertTrue(np.allclose(div(x), np.array([1.0, 0.98, 0.9506, 0.912576])))
        # move it back again
        ratios -= 0.01
        self.assertTrue(np.allclose(div(x), np.array([1.0, 0.99, 0.9702, 0.941094])))
