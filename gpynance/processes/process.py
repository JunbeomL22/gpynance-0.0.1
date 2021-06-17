from gpynance import gvar

class Process:
    def __init__(self, init, xp = gvar.xp, dtype = gvar.dtype, name = "", target = "cuda"):
        self.init = init
        self.xp = xp
        self.target = target
        self.dtype = dtype
        self.name = name
