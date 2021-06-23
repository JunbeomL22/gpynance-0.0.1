
# gpynance
from gpynance import gvar
from gpynance.utils import myexception
from gpynance.parameters import parameter
from gpynance.utils import utils, data, referencedate
# other packages
import numpy as np
import QuantLib as ql
from scipy.interpolate import interp1d

class Dividend(parameter.Parameter):
    """
    Dividend(dates, ratios, ref_date, dtype = gvar.dtype, name ="")
    
    The first input must be QuantLib.Date type. 
    This choice is for theta calculation. 
    Dividend paying dates are usually fixed. 
    Thus, when an evaluation date is moved, we should have the closer dividend dates. 
    This effect would be crucial if the closest dividend date is T + Day(1).
    
    ratios is the observable of DividendRatio. 
    If data (= ratios) notifies, the interpolation attribute in Dividend is updated.
    The value of ratios is like 0.002, 0.003.
    times can be ql.Date type.
    
    cupy interpolation is not defined, so xp = np by default
    """
    def __init__(self, dates, ratios, ref_date, xp = np, dtype = gvar.dtype, name =""):
        super().__init__([ref_date, ratios],
                         xp, ref_date, dtype, name)
        if len(dates) != len(ratios.data):
            raise myexception.MyException("The times and ratios have different length", self, self.name)
        
        self.whattimeis = utils.WhatTimeIs(ref_date, xp = self.xp, dtype = self.dtype)
        
        if not all(type(e) == ql.Date for e in dates):
            raise myexception.MyException("The first input must be iterable QuantLib.Date type", self, self.name)
        
        self.dates = dates
        self.times = self.whattimeis(dates)
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
    
    def update(self, obs, *args):
        """
        The action after an observable nofities a change.
        """
        #import pdb;pdb.set_trace()
        if isinstance(obs, referencedate.ReferenceDate):
            self.times = self.whattimeis(self.dates)
            if self.xp.isclose(self.times[0], 0.0) and len(self.times) < len(self.ratios):
                self.ratios = self.ratios[1:]
            if not self.xp.isclose(self.times[0], 0.0) and len(self.times) == len(self.ratios):
                self.times = self.xp.insert(self.times, 0, 0.0, axis=0)
                self.ratios = self.xp.insert(self.ratios, 0, 0.0, axis=0)

        if isinstance(obs, data.Data):
            self.ratios = self.xp.array(obs.data, dtype=self.dtype)
            if self.xp.isclose(self.times[0], 0.0) and len(self.times) > len(self.ratios):
                self.ratios = self.xp.insert(self.ratios, 0, 0.0, axis=0)
            if not self.xp.isclose(self.times[0], 0.0) and len(self.times) == len(self.ratios):
                self.times = self.xp.insert(self.times, 0, 0.0, axis=0)
                self.ratios = self.xp.insert(self.ratios, 0, 0.0, axis=0)
        
        self.accum_deduction = self.xp.multiply.accumulate( 1.0 - self.ratios )
        self.interp=interp1d(self.times, self.accum_deduction, kind='previous', fill_value="extrapolate")

        
