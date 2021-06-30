import gpynance
#-
import QuantLib as ql
import numpy as np

ref = gpynance.ReferenceDate(ql.Date(4, 1, 2021))
dtg = gpynance.DateTimeGrid(ref, ref.date + ql.Period("1W"))
path_data = np.array(np.arange(24).reshape(2, 2, 6), dtype='float32')

path_data1 = path_data[:, 0, :]
path_data2 = path_data[:, 1, :]

past1= {ql.Date(1, 1, 2021): -1.0, ql.Date(30, 12, 2020): -2.0, ql.Date(29, 12, 2020): -3.0}
past2= {ql.Date(1, 1, 2021): -4.0, ql.Date(30, 12, 2020): -5.0, ql.Date(29, 12, 2020): -6.0}

path1 = gpynance.SinglePath(dtg, path_data1, past1, "the first path", xp = np)
path2 = gpynance.SinglePath(dtg, path_data2, past2, "the second path", xp = np)

multi_path = gpynance.MultiPath(dtg, [path1, path2])

d0 = ql.Date(6, 1, 2021)
d1 = ql.Date(1, 1, 2021)
d2 = ql.Date(31, 12, 2020)
d3 = ql.Date(30, 12, 2020)

check0 = multi_path(d0)
check1 = multi_path(d1)
check2 = multi_path(d2)
check3 = multi_path(d3)

check4 = multi_path(start_date = ql.Date(30, 12, 2020), end_date = d0, after_ref=False)

print("\n(say) simulated path: \n")
print(path_data, "\n")

print(", on datetimegrid: \n")
print(dtg.dates, "\n")

print("and (say) past_vals: \n")
print(past1, "\n")
print(past2, "\n")

print("The interfaces of MultiPath are as follows\n ")

print(f"multi_path({d0}): \n [ {check0[0]}, \n\n {check0[1]} ]\n")
print(f"multi_path({d1}): \n [ {check0[1]}, \n\n {check1[1]} ]\n")
print(f"multi_path({d2}) (NOTE! there is no past data on <{d2}>, so spot values are retrieved): \n [ {check0[0]}, \n\n {check0[1]} ]\n")

print("you can slice paths, e.g., multi_path(ql.Date(5, 1, 2021), num=3) gives \n")
print("[ ", multi_path(ql.Date(5, 1, 2021), num=3)[0], ", \n")
print(multi_path(ql.Date(5, 1, 2021), num=3)[1], " ]")
print("\nNOTE! the first column is the past data \n")

print("or multi_path(start_date = ql.Date(30, 12, 2020), end_date = ql.Date(7, 1, 2021), after_ref = False) gives \n")
t = multi_path(start_date = ql.Date(30, 12, 2020), end_date = ql.Date(7, 1, 2021), after_ref = False)
print("[ ", t[0], ", \n")
print(t[1], " ]")
print("\nNOTE! it slices in a slightly different way from the case using <num = n>.  \n")
print("if you set after_ref = True, then you will have")

t = multi_path(start_date = ql.Date(30, 12, 2020), end_date = ql.Date(7, 1, 2021), after_ref = True)
print("[ ", t[0], ", \n")
print(t[1], " ] \n")

print("If you want to clone path with slicing, do, for example, multi_path.clone_upto( ql.Date(7, 1, 2021) )")
