import QuantLib as ql
import numpy as np
import cupy as cp
from gpynance.utils.myexception import MyException, MyFunctionException

def whattimeis(t, ref_date=None, dc=None, dtype=None):
    """
    whattimeis(t, ref_date=None, dc=None)
    If type(t) == ql.Date, it returns the year fraction w.r.t ref_date. Otherwise, this return t
    """
    floattype = (float, np.float16, np.float32, np.float64, cp.float16, cp.float32, cp.float64)
    arraytype = (np.ndarray, cp.ndarray, list, tuple)
    if type(t) in floattype:
        return t
    elif type(t) == ql.Date:
        if ref_date is None:
            raise MyFunctionException("ref_date must be input together", "whattimeis")
        if dc is None:
            return (t - ref_date.d) / 365.0
        else:
            return dc.yearFraction(ref_date.d, t)
    elif type(t) in arraytype:
        if type(t[0]) in floattype:
            return t
        elif type(t[0]) == ql.Date:
            t = np.array(t)
            if dtype is None:
                dtype = 'float32'
            t = np.array(t-ref_date.d, dtype=dtype) / 365.0
            return t
        else:
            raise MyFunctionException("The element type in the iterable input can't infer the action", "whattimeis")
    else:
        raise MyFunctionException("The input can't infer the action", "whattimeis")
    
