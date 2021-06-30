from gpynance import gvar, null_parameter
from gpynance.processes import process
from gpynance.parameters import volatility
# - 
import cupy as cp
import numpy as np

import time

class GbmProcess(process.Process1D):
    def __init__(self, init, vol, quanto, risk_free, dividend_ratio=null_parameter.null_dividend,
                 repo=null_parameter.null_yts, xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        
        super().__init__(init, xp, dtype, name, target)
        # -
        self.vol = vol
        self.quanto = quanto
        self.risk_free = risk_free
        self.repo = repo
        self.dividend_ratio = dividend_ratio

        self.cache_forward = False
            
    def evolve(self, m, t, dt):
        self.apply_volatility(m, dt, self.quanto) #quanto is taken together for minimizing numba compilation
        m = self.xp.exp(m)
        m = self.apply_forward(m, t)
        return m

    def cache(self, dtg):
        t = dtg.times
        if self.target == "cuda":
            self.cached_forward = cp.array(self.forward(t), dtype = self.dtype)
        else:
            self.cached_forward = np.array(self.forward(t), dtype = self.dtype)
            
    def apply_volatility(self, m, dt, quanto):
        return self.vol.apply_volatility(m, dt, quanto)

    def apply_quanto(self, m, dt):
        return self.quanto.apply_quanto(m, self.vol.sigma, dt)

    def apply_forward(self, m, t):
        #if self.target == "cuda":
        #    fd = cp.array(self.forward(t), dtype = self.dtype)
        #else:
        #    fd = np.array(self.forward(t), dtype = self.dtype)
        return m*self.cached_forward

    def forward(self, t):
        """
        This method uses dividend, risk_free rates, etc.
        Since the parameter objects usually use numpy by default (you can change it), 
        this method would highly likely return numpy array.
        
        Thus, you may need to convert it to cupy array explicitly later on.
        """
        div_deduct = self.dividend_ratio(t)
        disc_rate = self.risk_free.discount(t)
        disc_repo = self.repo.discount(t)
        res = self.init.data*div_deduct * disc_repo / disc_rate
        return res
