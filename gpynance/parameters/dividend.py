from gpynance.utils.data import Data
from gpynance.utils.observer import Observer, Observable
import gpynance.gvar
from gpynance.utils.myexception import MyException
from scipy.interpolate import interp1d
import numpy as np

class Dividend(Observer):
    """
    Dividend(times, ratios, ref_date = gvar.ref_date, dtype = gvar.dtype, name ="")
    
    ratios is the observable of DividendRatio. 
    If data (= ratios) notifies, the interpolation attribute in Dividend is updated.
    The value of ratios is like 0.002, 0.003.
    times can be ql.Date type.
    
    cupy interpolation is not defined, so xp = np by default
    """
    def __init__(self, times, ratios, ref_date = gvar.eval_date, dtype = gvar.dtype, name =""):
        super().__init__(ratios)
        self.dtype = dtype
        self.ref_date = ref_date
        
        if all(isinstance(t, ql.Date) for t in times):
            self.times = np.array([ql.ActualActual().yearFraction(ref_date.d, t) for t in times], dtype=self.dtype)
        elif all(type(t) in (float, np.float16, np.float32, np.float64) for t in times):
            self.times = np.array(times, dtype=self.dtype)
        else:
            raise MyException("The element type of time is obscure", self, name)

        self.ratios = np.array(ratios.data, dtype = self.dtype)
        self.accum_deduction = np.multiply.accumulate( 1.0 - self.ratios )
        
        self.interp=interp1d(self.times, self.accum_deduction, kind='previous', fill_value="extrapolate")

    def __call__(self, x):
        return self.interp(x)
        
    def update(self, data, *args):
        self.ratios = np.array(data.data, dtype=self.dtype)
        self.accum_deduction = np.multiply.accumulate( 1.0 - self.ratios )
        self.interp=interp1d(self.times, self.accum_deduction, kind='previous', fill_value="extrapolate")
        
