from gpynance.parameters.parameter import Parameter
# -
import QuantLib as ql

class Ibor:
    def __init__(self, yts, period, dc, past={}):
        self.ref_date = yts.ref_date
        self.period = period
        self.yts = yts
        self.past = past
        self.dc = dc

    def fixing(self, date):
        if date in self.past.keys():
            return self.past[date]
        else:
            ref = self.yts.ref_date.date
            return self.yts.forward(ref, ref + self.period, compounding="simple")

class CD91(Ibor):
    def __init__(self, yts, dc, past={}):
        super().__init__(yts, ql.Period("91D"), dc, past)


class OvernightIndex:
    def __init__(self):
        pass
