import unittest
from gpynance.parameters import curve
from gpynance.utils import referencedate
from gpynance.utils import data
from gpynance.utils import utils
#-
import numpy as np
import QuantLib as ql

class TestCurve(unittest.TestCase):
    def test_curve_methods(self):
        """
        to test methods of ZeroCurve
        """
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dates = [ref_date.date + ql.Period(f"{i}Y") for i in range(1, 4)]
        w = utils.WhatTimeIs(ref_date, dtype='float64')
        x = w(dates)
        rates = data.Data([0.01, 0.02, 0.03])
        zc = curve.ZeroCurve(dates, rates, ref_date = ref_date, xp = np, dtype = 'float64')
        self.assertTrue( np.allclose(zc(x), np.array([0.01, 0.02, 0.03])) )
        self.assertTrue( np.allclose(np.exp( -x * rates.data), zc.discount(x)) )

        forward_method = zc.forward(1.0, np.array([2.0, 3.0]), compounding = 'simple')
        forward_hand = np.array([np.exp(-0.01 + 0.04)-1.0, (np.exp(-0.01 + 0.09)-1.0)/2.0])
        self.assertTrue(np.allclose(forward_method, forward_hand))
        
        rates += 0.01
        self.assertTrue( np.allclose(zc(x), np.array([0.02, 0.03, 0.04])) )
        rates -= 0.01
        self.assertTrue( np.allclose(zc(x), np.array([0.01, 0.02, 0.03])) )

    def test_curve_observables(self):
        """
        to test the purturbation effect of ZeroCurve observables
        """
        ref_date = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dates = [ref_date.date + ql.Period(f"{i}Y") for i in range(1, 4)]
        w = utils.WhatTimeIs(ref_date, dtype='float64')
        x = w(dates)
        rates = data.Data([0.01, 0.02, 0.03])
        zc = curve.ZeroCurve(dates, rates, ref_date = ref_date, xp = np, dtype = 'float64')

        # data purturbation. The following will be necessary for rho calculation
        rates += 0.01
        self.assertTrue( np.allclose(zc(x), np.array([0.02, 0.03, 0.04])) )
        rates -= 0.01
        self.assertTrue( np.allclose(zc(x), np.array([0.01, 0.02, 0.03])) )

        # ref_date purturbation. The following will be used in theta calculation
        one_day = ql.Period("1D")
        dates = [ref_date.date + ql.Period(f"{i}D") for i in range(1, 11)]
        d_before = zc.discount(dates)
        ref_date += one_day
        d_after = zc.discount(dates)
        ref_date -= one_day
        self.assertTrue(all(d_after[1:] == d_before[:-1]))
