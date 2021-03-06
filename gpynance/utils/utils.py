from gpynance.utils import myexception
from gpynance import gvar
from gpynance.utils import referencedate
#-
import QuantLib as ql
import numpy as np
import cupy as cp

import time
#-

class WhatTimeIs:
    def __init__(self, ref_date, dtype=gvar.dtype, dc=ql.ActualActual(), xp=np):
        self.ref_date = ref_date
        self.dc = dc
        self.dtype = dtype
        self.xp=xp

        self.floattype = (float, np.float16, np.float32, np.float64, cp.float16, cp.float32, cp.float64)
        self.arraytype = (np.ndarray, cp.ndarray, list, tuple)
    def __call__(self, t):
        """
        whattimeis(t, ref_date=None, dc=None)
        If type(t) == ql.Date, it returns the year fraction w.r.t ref_date. Otherwise, this return t
        """
        
        if type(t) in self.floattype:
            return t
        elif type(t) == ql.Date:
            if self.ref_date is None:
                raise myexception.MyFunctionException("ref_date must be input together", "whattimeis")
            if self.dc is None:
                return (t - self.ref_date.date) / 365.0
            else:
                return self.dc.yearFraction(self.ref_date.date, t)
        elif type(t) in self.arraytype:
            if type(t) in (np.ndarray, cp.ndarray) and t.shape == ():
                return t
            elif type(t[0]) in self.floattype:
                return t
            elif type(t) == cp._core.core.ndarray and type(t[0]) == cp._core.core.ndarray:
                return t
            elif type(t[0]) == ql.Date:
                t = np.array(t)
                t = np.array(t-self.ref_date.date, dtype=self.dtype) / 365.0
                if self.xp == np:
                    return t
                else:
                    return self.xp.array(t)
            else:
                raise myexception.MyFunctionException("The element type in the iterable input can't infer the action", "whattimeis")
        else:
            raise myexception.MyFunctionException("The input can't infer the action", "whattimeis")



