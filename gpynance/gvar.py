import numpy as np
import cupy as cp
import QuantLib as ql
from gpynance.utils import referencedate

dtype = 'float32'
xp = cp
eval_date = referencedate.ReferenceDate(ql.Date.todaysDate())
eval_maturity = eval_date.d + ql.Period("3Y")+ql.Period("5D")
base_calendar = ql.SouthKorea() # this is basically for simulation. Using joint calendar is not much beneficial

#null_yts = curve.ZeroCurve(eval_date, [0.0, 30.0], [0.0, 0.0])
#null_interp=interp1d([0.0, 30.0], [0.0, 0.0], kind='previous')
