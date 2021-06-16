from gpynance.utils.observer import Observer
from gpynance import gvar
import QuantLib as ql

class Parameter(Observer):
    def __init__(self, observables, xp, ref_date, dtype = gvar.dtype, name =""):
        super().__init__(observables)
        self.xp = xp
        self.dtype = dtype
        self.ref_date = ref_date
        self.name = name

    def set_times(self, times):
        if all(isinstance(t, ql.Date) for t in times):
            self.times = self.xp.array([ql.ActualActual().yearFraction(self.ref_date.date, t) for t in times], dtype=self.dtype)
        elif all(type(t) in (float, self.xp.float16, self.xp.float32, self.xp.float64) for t in times):
            self.times = self.xp.array(times, dtype=self.dtype)
        else:
            raise MyException("The element type of time is obscure", self, self.name)
        
