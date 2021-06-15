import QuantLib as ql

class ReferenceDate:
    def __init__(self, date=ql.Date.todaysDate()):
        self.date = date
