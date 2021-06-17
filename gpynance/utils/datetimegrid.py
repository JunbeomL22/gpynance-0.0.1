from gpynance import gvar
from gpynance.utils import myexception
from gpynance.utils import observer
from gpynance.utils import referencedate
#-
import QuantLib as ql

class DateTimeGrid(observer.Observer):
    def __init__(self, start_date,
                 end_date,
                 calendar = gvar.base_calendar,
                 mand_dates = [],
                 only_mand = False,
                 xp = gvar.xp,
                 dtype=gvar.dtype):
        '''
        DateTimeGrid(self, start_date,
                 end_date,
                 calendar = gvar.base_calendar,
                 mand_dates = [],
                 xp = gvar.xp,
                 dtype=gvar.dtype)

        note: start_date (ReferenceDate) is observable

        dtg.times (the first element is 0)
        dtg.dt (the first element is 0)
        dtg.sqdt == sqrt(dtg.dt)
        
        ex)
        v = DateTimeGrid(start_date = Date(2,6,2021), end_date = Date(2, 6, 2024), 
                         only_mand = True, mand_dates = [ql.Date(1, 1, 2022), ql.Date(1, 1, 2023)])
        v.times => array([0.58356166, 1.5835617 ], dtype=float32)
        v.dt => array([0., 1.], dtype=float32)
        '''
        super().__init__([start_date])
        self.xp = xp
        self.dtype = dtype
        self.ref_date = start_date
        self.calendar = calendar
        self.mand_dates = mand_dates
        self.only_mand  = only_mand
        self.mand_dates = mand_dates
        self.calendar = calendar
        self.xp = xp

        self.maturity = calendar.adjust(end_date)

        if self.ref_date > self.maturity:
            raise myexception.MyException("start_date > maturity", self)

        self.calculate()
        
    def calculate(self):
        if self.only_mand:
            self.dates = []
            tm = []
        else:
            self.dates = [self.ref_date.date]
            tm = [0.0]
        _days = self.maturity-self.ref_date.date
        days = _days if _days > 0 else 0

        d = self.ref_date.date
        
        mand_tm=[]
        dc = ql.ActualActual()
        for i in range(days):
            d = self.ref_date.date + ql.Period(i+1, ql.Days)
            if (((not self.only_mand) and self.calendar.isBusinessDay(d)) or (d in self.mand_dates)):
                self.dates.append(d)
                tm.append(dc.yearFraction(self.ref_date.date, d))
                if (d in self.mand_dates):
                    mand_tm.append(dc.yearFraction(self.ref_date.date, d))
                          
        self.times = self.xp.array(tm, dtype=self.dtype)
        self.mand_times = self.xp.array(mand_tm, dtype=self.dtype)
        self.dt = self.xp.zeros(self.times.shape[0], dtype=self.dtype)
        self.dt[1:] = self.times[1:] - self.times[:-1]
        self.sqdt = self.xp.sqrt(self.dt)

    def update(self, obs, *args):
        self.calculate()
