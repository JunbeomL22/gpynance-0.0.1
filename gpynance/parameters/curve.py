from scipy.interpolate import interp1d
import numpy as np
import QuantLib as ql
from gpynance.utils.myexception import MyException

class ZeroCurve:
    def __init__(self, ref_date, times, rates, dc = ql.ActualActual(), xp=np, dtype='float32'):
        self.xp = xp
        self.dtype=dtype
        self.ref_date = ref_date
        self.dc = dc
        self.times = self.xp.array(times, self.dtype)
        self.rates = self.xp.array(rates, self.dtype)
        if len(times) != len(rates):
            raise MyException("data of times and rates have different length", self)

        if not self.xp.isclose(self.times[0], 0.0):
            self.times = self.xp.insert(self.times, 0, 0.0, axis=0)
            self.rates = self.xp.insert(self.rates, 0, 0.0, axis=0)
            
        self.discounts = self.xp.exp(- self.times * self.rates)
        self.interp = interp1d(self.times, self.discounts)

    def discount(self, t):
        if isinstance(t, ql.Date):
            t= self.dc.yearFraction(self.ref_date.d, t)
            
        if type(t) not in [float, self.xp.float32, self.xp.float64, self.xp.float16, self.xp.ndarray]:
            raise MyException("input for discount is not defined", self)

        if type(t) in [float, self.xp.float16, self.xp.float32, self.xp.float64] and t > self.times[-1]:
            raise MyException("input for discount is longer than data", self)

        if type(t) == self.xp.ndarray and t[-1] > self.times[-1]:
            raise MyException("input for discount is longer than data", self)

        return self.interp(t)

    def simple_forward(self, t1, t2=None):
        if type(t1) == ql.Date and type(t2) == ql.Date:
            t1 = self.dc.yearFraction(self.ref_date.d, t1)
            t2 = self.dc.yearFraction(self.ref_date.d, t2)
            
        if type(t1) == ql.Date and t2 == None:
            t1 = self.dc.yearFraction(self.ref_date.d, t1)
            t2 = self.dc.yearFraction(self.ref_date.d, t1) + 0.00005

        if t2 == None:
            t2 = t1 + 0.00005
            
        tau = t2-t1

        res = (self.discount(t1) / self.discount(t2) - 1.0)/tau
        return res

