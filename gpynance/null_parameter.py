from gpynance.parameters import curve
from gpynance.parameters import dividend
from gpynance.utils import data
from gpynance.utils import referencedate
from gpynance import gvar
#-
import QuantLib as ql

ref = referencedate.ReferenceDate()
null_yts = curve.ZeroCurve([0.0, 100.0], data.Data([0.0, 0.0]), ref_date = ref)
null_dividend = dividend.Dividend([ref.date, ref.date + ql.Period("100Y")], data.Data([0.0, 0.0]), ref_date = ref)

