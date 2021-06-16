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
