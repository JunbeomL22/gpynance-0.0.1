from gpynance.utils.observer import Observable
from gpynance import gvar
#-
import numpy as np
import cupy as cp

class Data(Observable):
    def __init__(self, data, xp = np, name="", dtype = gvar.dtype):
        super().__init__()
        self.xp = xp
        self.dtype=dtype
        self.data = data #self.xp.array(data, dtype = self.dtype)
        
    def __iadd__(self, x):
        if type(self.data) in (np.ndarray, cp.ndarray):
            self.data += x
        elif type(self.data) in (list, tuple):
            for i, e in enumerate(self.data):
                self.data[i] += x
        else:
            self.data += x

        self.notify()
        return self

    def __isub__(self, x):
        if type(self.data) in (np.ndarray, cp.ndarray):
            self.data -= x
        elif type(self.data) in (list, tuple):
            for i, e in enumerate(self.data):
                self.data[i] -= x
        else:
            self.data -= x
        self.notify()
        return self
