import QuantLib as ql
from gpynance import gvar
from gpynance.utils.myexception import MyException

class ConstantVolatility:
    def __init__(self, sigma, ref_date=gvar.eval_date, name="ConstantVolatility"):
        self.ref_date = ref_date
        self.name = name
        self.sigma=sigma

    def local_vol(self, t, x):
        return self.sigma

class ImpliedVolatility:
    """
    ImpliedVolatility(times, strikes, data, ref_date=gvar.eval_date,
                 xp=gvar.xp, dtype = gvar.dtype, name="undefined")
    """
    def __init__(self, times, strikes, data, ref_date=gvar.eval_date,
                 xp=gvar.xp, dtype = gvar.dtype, name="undefined"):
        self.xp = xp
        self.dtype = dtype
        self.ref_date = ref_date
        self.name = name
        
        if all(isinstance(t, ql.Date) for t in times):
            self.times = self.xp.array([ql.ActualActual().yearFraction(ref_date.d, t) for t in times], dtype=self.dtype)
        elif all(type(t) in (float, xp.float16, xp.float32, xp.float64) for t in times):
            self.times = self.xp.array(times, dtype=self.dtype)
        else:
            raise MyException("The element type of time is obscure", self, name)

        self.strikes = self.xp.array(strikes, dtype = self.dtype)
        self.data = self.xp.array(data, dtype = self.dtype)

class StrikeImpliedVolatility:
    def __init__(self, imvol, forward_engine, forwardsname="undefined"):
        self.ref_date = ref_date
        self.name = name
        self.forward = forward

class Quanto:
    """
    Quanto(corr = -0.01, sigma = 0.01, name = "<KRW, SnP>)
    """
    def __init__(self, sigma, rho, name="undefined"):
        self.sigma = sigma
        self.rho = rho
        
