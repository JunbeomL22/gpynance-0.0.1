import numpy as np

class FixedCoupon:
    """
    FixedCoupon(c)

    c is a float form, e.g., 0.02 (= 2%)
    """
    def __init__(self, c):
        self.c = c

    def __call__(self, x=None):
        return self.c
        

class FixedCouponRedemption:
    """
    FixedCouponRedemption(c)

    c is a float form, e.g., 0.02 (= 2%)
    """
    def __init__(self, c):
        self.c = c

    def __call__(self, x=None):
        return 1.0 + self.c


class Performer:
    def __init__(self, lower=-np.Inf, upper = np.Inf, xp = np):
        self.lower = lower
        self.upper = upper
        self.xp = xp

    def __call__(self, x):
        res = self.xp.maximum(x, self.lower)
        res = self.xp.minimum(res, self.upper)
        return res
