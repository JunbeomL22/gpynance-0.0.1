import unittest
from gpynance.utils import referencedate
from gpynance.utils import datetimegrid
#-
import QuantLib as ql
import numpy as np
import cupy as cp


class TestReference(unittest.TestCase):
    """
    To Check the change of reference date is updated to parameters, e.g., curve and dividend
    """
    def test_referencedate(self):
        ref_date = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
        dtg = datetimegrid.DateTimeGrid(ref_date, ref_date.date + ql.Period("10D"))

        self.assertTrue(cp.isclose(dtg.dt[0], 0.0))
        self.assertTrue(all(cp.isclose(dtg.dt[1:4], 0.00273973)))
        self.assertTrue(cp.isclose(dtg.dt[5], 0.00821918))
        self.assertTrue(all(cp.isclose(dtg.dt[6:], 0.00273973)))
        
        one_day = ql.Period("1D")
        ref_date += one_day
        self.assertTrue(cp.isclose(dtg.dt[0], 0.0))
        self.assertTrue(all(cp.isclose(dtg.dt[1:3], 0.00273973)))
        self.assertTrue(cp.isclose(dtg.dt[4], 0.00821918))
        self.assertTrue(all(cp.isclose(dtg.dt[5:], 0.00273973)))

        ref_date -= one_day
        self.assertTrue(cp.isclose(dtg.dt[0], 0.0))
        self.assertTrue(all(cp.isclose(dtg.dt[1:4], 0.00273973)))
        self.assertTrue(cp.isclose(dtg.dt[5], 0.00821918))
        self.assertTrue(all(cp.isclose(dtg.dt[6:], 0.00273973)))
