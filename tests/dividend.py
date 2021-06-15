import unittest
from gpynance.parameters import dividend
from gpynance.utils import referencedate
from gpynance.utils import data
#-
import numpy as np
class TestDividend(unittest.TestCase):
    def test_dividend(self):
        ref_date = referencedate.ReferenceDate()
        times = [1.0, 2.0, 3.0]
        ratios = data.Data([0.01, 0.02, 0.03])
        
        div = dividend.Dividend(times, ratios, ref_date = ref_date, xp = np)

        accum_div = div(times)
        test_accum_div = np.multiply.accumulate(1.0-np.array(ratios.data, dtype='float32'))
        self.assertEqual(accum_div.tolist(), test_accum_div.tolist())
        
