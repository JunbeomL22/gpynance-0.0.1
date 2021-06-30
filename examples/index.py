from gpynance.parameters import index, curve
from gpynance.utils import data, referencedate
# -
import numpy as np
import QuantLib as ql

ref_date = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
times = [1.0]
rates = data.Data([0.02])
yts = curve.ZeroCurve(times, rates, ref_date)

past = {ql.Date(30, 12, 2020): 0.01, ql.Date(29, 12, 2020): 0.1}
dc = ql.Actual365Fixed()

cd = index.CD91(yts, dc, past)

cd.fixing(ql.Date(4, 1, 2021))


print("")
print(f"past data: {past} and constant rate curve of 0.02")
print(f"fixing rate at the reference date {ref_date.date}: ")
print(cd.fixing(ref_date.date), "\n")

d = ql.Date(1, 6, 2021)
print(f"fixing rate at the reference date {d}: ")
print(cd.fixing(d), "\n")

print(f"fixing rate at {ql.Date(30, 12, 2020)}: ")
print(cd.fixing(ql.Date(30, 12, 2020)), "\n")

print(f"fixing rate at {ql.Date(29, 12, 2020)}: ")
print(cd.fixing(ql.Date(29, 12, 2020)), "\n")

print("when there is no past data, fixing method returns the forward rate at the reference date")
print(f"fixing rate at {ql.Date(31, 12, 2020)}: ")
print(cd.fixing(ql.Date(31, 12, 2020)), "\n")
