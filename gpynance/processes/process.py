from gpynance import gvar

class Process:
    def __init__(self, init, xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        self.init = init
        self.xp = xp
        self.target = target
        self.dtype = dtype
        self.name = name

class Process1D(Process):
    """
    Examples are classic Black Scholes model, local volatility model, etc
    """
    def __init__(self, init, xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        super().__init__(init, xp = xp, dtype = dtype, name = name, target = target)
        self.dimension = 1

class Process2D(Process):
    """
    Examples are stochastic volatiltiy, G2++, etc
    """
    def __init__(self, init, xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        super().__init__(init, xp = xp, dtype = dtype, name = name, target = target)
        self.dimension = 2
        
class Processes:
    def __init__(self, processes, corr = [0.0], name = ""):
        self.processes = processes
        self.num_procs = len(self.processes)
        self.corr  = corr
        self.name  = name
        self.num_random = 0
        for p in self.processes:
            self.num_random += p.dimension

    def __getitem__(self, i):
        return self.processes[i]
