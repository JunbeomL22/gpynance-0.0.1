from gpynance.utils import observer
import QuantLib as ql

class ReferenceDate(observer.Observable):
    def __init__(self, date=ql.Date.todaysDate()):
        super().__init__()
        self.date = date

    def __iadd__(self, period):
        self.date += period
        self.notify()
        return self

    def __isub__(self, period):
        self.date -= period
        self.notify()
        return self

    def __add__(self, period):
        return self.date + period
    
    def __sub__(self, period):
        return self.date - period
    
    def __gt__(self, d):
        return self.date > d
    
    def __ge__(self, d):
        return self.date >= d
    
    def __lt__(self, d):
        return self.date < d
    
    def __le__(self, d):
        return self.date <= d
