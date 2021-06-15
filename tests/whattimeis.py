import unittest
from gpynance.utils import utils
from gpynance.utils import referencedate
from gpynance import gvar

# --
import QuantLib as ql
import numpy as np
import cupy as cp

class TestWhatTimeIs(unittest.TestCase):
    def test_date(self):
        refdate = referencedate.ReferenceDate(ql.Date(1, 1, 2021))
        dc = ql.ActualActual()
        d = ql.Date(2, 2, 2022)
        time = dc.yearFraction(refdate.date, d)
        whattimeis = utils.WhatTimeIs(refdate, dc = dc, xp=np)
        self.assertEqual(whattimeis(d), time)

        # check date list to numpy
        dlist = [ql.Date(2, 2, 2022), ql.Date(2, 2, 2023)]
        res = whattimeis(dlist)
        times = np.array([dc.yearFraction(refdate.date, dlist[0]), dc.yearFraction(refdate.date, dlist[1])], dtype=gvar.dtype)
        self.assertTrue(np.allclose(res, times))

        #check numpy date to cupy
        darray = np.array([ql.Date(2, 2, 2022), ql.Date(2, 2, 2023)])
        whattimeis = utils.WhatTimeIs(refdate, dc = dc, xp = cp)
        res = whattimeis(darray)
        self.assertTrue(cp.allclose(res, cp.array(times, dtype=gvar.dtype)))

        
