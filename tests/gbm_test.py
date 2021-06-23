import unittest
from gpynance.processes import gbm
from gpynance.parameters import volatility
# -
#import numpy as np
class TestGbm(unittest.TestCase):
    def test_gbm(self):

        self.assertTrue(True)
        #vol = volatility.ConstantVolatility(sigma = 0.2)
        #quanto = volatility.Quanto(sigma = 0.01, rho = -0.2)

        #proc = gbm.GbmProcess
