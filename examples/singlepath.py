from gpynance.engines.montecarlo import path
from gpynance.utils import datetimegrid, referencedate
#-
import QuantLib as ql
import numpy as np

ref = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
dtg = datetimegrid.DateTimeGrid(ref, ref.date + ql.Period("1W"))
path_data = np.array(np.arange(24).reshape(4, 6), dtype='float32')
past= {ql.Date(1, 1, 2021): -1.0, ql.Date(30, 12, 2020): -2.0, ql.Date(29, 12, 2020): -3.0}

singlepath = path.SinglePath(dtg, path_data, past, name = "test")

d0 = ql.Date(6, 1, 2021)
d1 = ql.Date(1, 1, 2021)
d2 = ql.Date(31, 12, 2020)
d3 = ql.Date(30, 12, 2020)

check0 = singlepath(d0)
check01 = singlepath(d0, 5)
check1 = singlepath(d1)
check2 = singlepath(d2)
check3 = singlepath(d3)

#print("\n(say) simulated path: \n")
#print(path_data, "\n")
#print(", on datetimegrid: \n")
#print(dtg.dates, "\n")
#print("and (say) past_vals: \n")
#print(past1, "\n")
#print(past2, "\n")
#print(f"path({d0}): \n {check0} \n")
#print(f"path({d1}): \n {check1} \n")
#print(f"path({d2}) (NOTE! there is no past data on <{d2}>, so spot values are retrieved): \n {check2} \n ")
#print("you can slice paths, e.g., path(ql.Date(5, 1, 2021), num=3) gives \n")
#print(path(ql.Date(5, 1, 2021), num=3))
#print("\nNOTE! the first column is the past data \n")
#print("If you want to clone path with slicing, do, for example, path.clone_upto(ql.Date(7, 1, 2021)")
