from gpynance import gvar
import QuantLib as ql
from gpynance.utils import myexception 

class DateTimeGrid:
    def __init__(self, start_date,
                 end_date,
                 calendar = gvar.base_calendar,
                 mand_dates = [],
                 only_mand = False,
                 xp = gvar.xp,
                 dtype=gvar.dtype):
        '''
        DateTimeGrid(self, start_date = gvar.eval_date,
                 end_date = gvar.eval_maturity,
                 calendar = gvar.base_calendar,
                 mand_dates = [],
                 xp = gvar.xp,
                 dtype=gvar.dtype)
        
        dtg.times (the first element is 0)
        dtg.dt (the first element is 0)
        dtg.sqdt == sqrt(dtg.dt)
        
        ex)
        v = DateTimeGrid(start_date = Date(2,6,2021), end_date = Date(2, 6, 2024), 
                         only_mand = True, mand_dates = [ql.Date(1, 1, 2022), ql.Date(1, 1, 2023)])
        v.times => array([0.58356166, 1.5835617 ], dtype=float32)
        v.dt => array([0., 1.], dtype=float32)
        '''
        self.xp = xp
        self.dtype = dtype
        self.ref_date = start_date
        self.calendar = calendar
        self.mand_dates = mand_dates
        if only_mand:
            self.dates = []
            tm = []
        else:
            self.dates = [self.ref_date]
            tm = [0.0]

        self.maturity = calendar.adjust(end_date)

        if start_date > self.maturity:
            raise myexception.MyException("start_date > maturity, location: DateTimeGrid", self)

        days = (self.maturity-start_date)

        d = self.ref_date
        
        mand_tm=[]
        dc = ql.ActualActual()
        for i in range(days):
            d = self.ref_date + ql.Period(i+1, ql.Days)
            if (((not only_mand) and calendar.isBusinessDay(d)) or (d in mand_dates)):
                self.dates.append(d)
                tm.append(dc.yearFraction(self.ref_date, d))
                if (d in mand_dates):
                    mand_tm.append(dc.yearFraction(self.ref_date, d))
                          
        self.times = xp.array(tm, dtype=self.dtype)
        self.mand_times = xp.array(mand_tm, dtype=self.dtype)
        self.dt = xp.zeros(self.times.shape[0], dtype=self.dtype)
        self.dt[1:] = self.times[1:] - self.times[:-1]
        self.sqdt = self.xp.sqrt(self.dt)
