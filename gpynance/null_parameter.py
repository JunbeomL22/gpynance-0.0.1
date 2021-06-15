from gpynance.parameters import curve
from gpynance.parameters import dividend
from gpynance.utils import data
from gpynance.utils import referencedate
from gpynance import gvar

null_yts = curve.ZeroCurve([0.0, 100.0], data.Data([0.0, 0.0]), ref_date = referencedate.ReferenceDate())
null_dividend = dividend.Dividend([0.0, 100.0], data.Data([0.0, 0.0]), ref_date = referencedate.ReferenceDate())

