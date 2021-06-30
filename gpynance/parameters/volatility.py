import QuantLib as ql
from gpynance import gvar
from gpynance.utils import myexception

from numba import cuda

@cuda.jit
def numba_apply_constant_vol(bm, dt, vol, quanto_sigma, quanto_rho):
    """
    This assumes 
    - bm is a brownian motion
    - dt[0] = 0.0
    """
    n = cuda.grid(1)
    if n < bm.shape[0]:
        c = bm.shape[2]
        for i in range(1, c):
            bm[n][0][i] = bm[n][0][i-1] + vol*bm[n][0][i] - 0.5*vol*vol*dt[i]
            bm[n][0][i] -= vol * quanto_sigma * quanto_rho * dt[i]

class ConstantVolatility:
    def __init__(self, sigma, name="", target = "cuda", thredsperblock=32):
        self.threadsperblock = thredsperblock
        self.name = name
        self.sigma = sigma
        self.target = target
        
    def __call__(self, t, x):
        return self.sigma

    def apply_volatility(self, m, dt, quanto):
        """
        Quanto is taken together here.
        This may be confusing, but this way is chosen for compiling numba jit function only once.
        """
        if self.target == "cuda":
            tpb = self.threadsperblock
            bpg = (m.shape[0] + (tpb-1)) // tpb
            numba_apply_constant_vol[bpg, tpb](m, dt, self.sigma, quanto.sigma, quanto.rho)
        else:
            raise myexception.MyException(f"A method applying volatility on {self.target} has not been defined", self, self.name)
        

class Quanto:
    '''
    Quanto(sigma, rho, name="")
    '''
    def __init__(self, sigma=0.0, rho=0.0, name=""):
        self.name = name
        self.sigma = sigma
        self.rho = rho

    def quanto_adjust(self, v):
        """
        quanto_adjust(self, v)
        
        This returns v * self.sigma * self.rho
        The amount of adjustment is quanto_adjust(self, vol) * dt
        """
        return v * self.sigma * self.rho

    def apply_quanto(self, m, v, dt):
        x = self.quanto_adjust(v)
        adj = x * dt
        return - adj + m
        

"""
class ImpliedVolatility:
    
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
    
    def __init__(self, sigma, rho, name="undefined"):
        self.sigma = sigma
        self.rho = rho
        
"""
