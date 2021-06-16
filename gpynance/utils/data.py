from gpynance.utils.observer import Observable
from gpynance import gvar
#-
import numpy as np

class Data(Observable):
    def __init__(self, data, xp = np, name="", dtype = gvar.dtype):
        super().__init__()
        self.xp = xp
        self.dtype=dtype
        self.data = self.xp.array(data, dtype = self.dtype)
        
    def __iadd__(self, x):
        self.data += x
        self.notify()
        return self

    def __isub__(self, x):
        self.data -= x
        self.notify()
        return self
