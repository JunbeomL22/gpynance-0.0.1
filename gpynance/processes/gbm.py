from gpynance import gvar, null_parameter
from gpynance.processes import process
from gpynance.parameters import volatility
# - 
import cupy as cp
import numpy as np

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
        m = self.apply_volatility(m)
        m = self.apply_quanto(m, dt)
        m = self.apply_forward(m, t)
        return m

    def apply_volatility(self, m):
        return self.vol.apply_volatility(m)

    def apply_quanto(self, m, dt):
        return self.quanto.apply_quanto(m, self.vol.sigma, dt)

    def apply_forward(self, m, t):
        if self.target == "cuda":
            fd = cp.array(self.forward(t), dtype = self.dtype)
        else:
            fd = np.array(self.forward(t), dtype = self.dtype)
        return m*fd

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
        res = div_deduct * disc_repo / disc_rate
        return res

    def cache_forward(self, t):
        if not self.cache_forward:
            if self.target == "cuda":
                self.cached_forward = cp.array(self.forward(t), dtype = self.dtype)
            else:
                self.cached_forward = np.array(self.forward(t), dtype = self.dtype)
            self.cache_forward = True
