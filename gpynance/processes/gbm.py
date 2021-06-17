from gpynance import gvar
from gpynance.processes import process
from gpynance.parameters import volatility

class GbmProcess(process.Process):
    def __init__(self, init, vol, quanto, risk_free, repo, dividend_ratio,
                 xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        
        super().__init__(init, xp, dtype, name, target)
        # -
        self.vol = vol
        self.quanto = quanto
        self.risk_free = risk_free
        self.repo = repo
        self.dividend_ratio = dividend_ratio
           
    def evolve(self, m, t, dt):
        if isinstance(self.vol, volatility.ConstantVolatility):
            

    def apply_volatility(self, m):
        return self.vol.apply_volatility(m)

    def apply_quanto(self, m, dt):
        return self.quanto.apply_quanto(m, self.vol.sigma, dt)

    def apply_forward(self, m, t, dt):
        fd = self.forward(t)
        return m*fd

    def forward(self, t):
        pass        
