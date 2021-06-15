from gpynance import gvar
from gpynance.utils.myexception import MyException
from scipy.interpolate import interp1d
from gpynance.parameters.parameter import Parameter
import numpy as np
from gpynance.utils import utils
import QuantLib as ql

class Dividend(Parameter):
    """
    Dividend(times, ratios, ref_date, dtype = gvar.dtype, name ="")
    
    ratios is the observable of DividendRatio. 
    If data (= ratios) notifies, the interpolation attribute in Dividend is updated.
    The value of ratios is like 0.002, 0.003.
    times can be ql.Date type.
    
    cupy interpolation is not defined, so xp = np by default
    """
    def __init__(self, times, ratios, ref_date, xp = np, dtype = gvar.dtype, name =""):
        super().__init__(ratios, xp, ref_date, dtype, name)
        if len(times) != len(ratios.data):
            raise MyException("The times and ratios have different length", self, self.name)
        
        self.whattimeis = utils.WhatTimeIs(ref_date, xp = self.xp, dtype = self.dtype)
        self.set_times(times)
        self.ratios = self.xp.array(ratios.data, dtype = self.dtype)

        if not self.xp.isclose(self.times[0], 0.0):
            self.times = self.xp.insert(self.times, 0, 0.0, axis=0)
            self.ratios = self.xp.insert(self.ratios, 0, 0.0, axis=0)
            
        self.accum_deduction = self.xp.multiply.accumulate( 1.0 - self.ratios )
        self.interp=interp1d(self.times, self.accum_deduction, kind='previous', fill_value="extrapolate")
        self.dc = ql.ActualActual()        
        
    def __call__(self, x):
        x = self.whattimeis(x)
        return self.interp(x)
    
    def update(self, data, *args):
        self.ratios = self.xp.array(data.data, dtype=self.dtype)
        self.accum_deduction = self.xp.multiply.accumulate( 1.0 - self.ratios )
        self.interp=interp1d(self.times, self.accum_deduction, kind='previous', fill_value="extrapolate")

        
