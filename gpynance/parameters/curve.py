from scipy.interpolate import interp1d
import numpy as np
import cupy as cp
import QuantLib as ql
from gpynance.utils.myexception import MyException
from gpynance.utils.observer import Observer, Observable
from gpynance.parameters.parameter import Parameter
from gpynance.utils.data import Data
from gpynance import gvar
from gpynance.utils import utils
from multipledispatch import dispatch

class ZeroCurve(Parameter):
    def __init__(self, times, rates, ref_date, dc = ql.ActualActual(), xp=np, dtype='float32', name=""):
        """
        ZeroCurve(times, rates, ref_date, dc = ql.ActualActual(), xp=np, dtype='float32', name =""):
        The rates is observable which must be a Data object.
        
        This interpolates on discounts not the rates.
        """
        super().__init__(rates, xp, ref_date, dtype, name)
        self.whattimeis = utils.WhatTimeIs(ref_date)
        if type(rates) != Data:
            raise MyException("rates must be Data object", self, name)
        if len(times) != len(rates.data):
            raise MyException("times and rates have different length", self, name)
        
        self.set_times(times)
        self.dc = dc
        self.rates = self.xp.array(rates.data, dtype=self.dtype)
        
        # if the first element of times is not 0.0, add it for the following interpolation
        if not self.xp.isclose(self.times[0], 0.0):
            self.times = self.xp.insert(self.times, 0, 0.0, axis=0)
            self.rates = self.xp.insert(self.rates, 0, 0.0, axis=0)
            
        self.discounts = self.xp.exp(- self.times * self.rates)
        self.interp = interp1d(self.times, self.discounts)

    def update(self, rates, *args):
        self.rates = self.xp.array(rates.data, dtype=self.dtype)
        self.discounts = self.xp.exp(- self.times * self.rates)
        self.interp = interp1d(self.times, self.discounts)

    @dispatch(object)
    def discount(self, t):
        t = self.whattimeis(t)
        return self.interp(t)

    @dispatch(object, object)
    def discount(self, t1, t2):
        t1 = self.whattimeis(t1)
        t2 = self.whattimeis(t2)
        return self.interp(t1) / self.interp(t1)
    
    @dispatch(object, object, str)
    def forward(self, t1, t2, compounding = "simple"):
        t1 = self.whattimeis(t1)
        t2 = self.whattimeis(t2)
        tau = t2-t1
        disc = self.discount(t1, t2)
        if compounding == "simple":
            return (disc -1.0) / tau
        elif compunding == "continuous":
            return - self.xp.log(disc) / tau
        else:
            raise MyException("The forward rate for the given compounding type has not been defined", self, self.name)

    @dispatch(object, str)
    def forward(self, t, compounding = "simple"):
        t = self.whattimeis(t)
        return self.forward(t, t + 0.0001, compounding)
        
