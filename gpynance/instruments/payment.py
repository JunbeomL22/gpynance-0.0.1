
import numpy as np

class FixedCoupon:
    """
    FixedCoupon(c)
    c is a float form, e.g., 0.02 (= 2%)
    """
    def __init__(self, c):
        self.c = c

    def __call__(self, multi_path, mask = None):
        n = multi_path(multi_path.dtg.ref_date.date, mask=mask)[0].shape[0]
        res = self.c * np.ones(n, dtype = x[0].dtype)
        return res

class FixedCouponRedemption:
    """
    FixedCouponRedemption(c)
    c is a float form, e.g., 0.02 (= 2%)
    """
    def __init__(self, c):
        self.c = c

    def __call__(self, multi_path, mask=None):
        n = multi_path(multi_path.dtg.ref_date.date, mask=mask)[0].shape[0]
        res = self.c * np.ones(n, dtype = x[0].dtype)
        return 1.0 + res

class ProfitPayment:
    def __init__(self, lowerbound, upperbound):
        self.date
        self.lowerbound = lowerbound
        self.upperbound = upperbound

    def __call__(self, multi_path, mask=None):
        x = multi_path(self.date, mask=mask)[0]
        res = x[0]
        n = len(x)
        if n == 1:
            return res
        
        for i in range(1, n):
            res = np.minimum(res, x[i])
            
        res = np.maximum(self.x, self.lowerbound)
        res = np.minimum(self.x, self.upperbound)
        return res
