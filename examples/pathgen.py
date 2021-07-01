import gpynance
# -
import QuantLib as ql
import numpy as np
import cupy as cp

import time

# - time setup
_mat = "2Y"
ref_date = gpynance.ReferenceDate(ql.Date(4, 1, 2021))
mat = ref_date + ql.Period(_mat)
dtg = gpynance.DateTimeGrid(ref_date, mat)

# - initial value. Note that these are observable
spot1 = gpynance.Data(1.0)
spot2 = gpynance.Data(2.0)

# - volatility setup, not observable
vol1 = gpynance.ConstantVolatility(sigma=0.2, name = "asset1's vol")
quanto1 = gpynance.Quanto(sigma = 0.0, rho = 0.0, name = "asset1's quanto (no quanto)")

vol2 = gpynance.ConstantVolatility(sigma = 0.1, name = "asset2's vol")
quanto2 = gpynance.Quanto(sigma = 0.02, rho = -0.1, name = "asset1's quanto")

corr = cp.identity(2)
corr[0, 1] = corr[1, 0] = 0.5

# - risk_free and dividend, see how they work with Data class. Recall that Data class is observable
risk_free_data1 = gpynance.Data([0.02])
risk_free_data2 = gpynance.Data([0.01])

risk_free1 = gpynance.ZeroCurve([dtg.times[-1]], risk_free_data1, ref_date)
risk_free2 = gpynance.ZeroCurve([dtg.times[-1]], risk_free_data2, ref_date)

div_dates1 = [ref_date + ql.Period("1D"), ref_date + ql.Period("2Y")]
div_dates2 = [ref_date + ql.Period("2D"), ref_date + ql.Period("2Y")]
dividend_data1 = gpynance.Data([0.01, 0.01])
dividend_data2 = gpynance.Data([0.0,  0.02])

dividend1 = gpynance.Dividend(div_dates1, dividend_data1, ref_date)
dividend2 = gpynance.Dividend(div_dates2, dividend_data2, ref_date)

null_curve = gpynance.null_yts

# - build processes
proc1 = gpynance.GbmProcess(spot1, vol1, quanto1, risk_free1, dividend1)
proc2 = gpynance.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
processes = gpynance.Processes([proc1, proc2], corr)

# - generating path
sim = 100000
batch = 25000
gen = gpynance.GpuPathGenerator(dtg, processes, num_simulation = sim, seed = 1, batch_size = batch)
gen.cache_cpu_path()
p1 = gen.path_cpu[:, 0, :]
p2 = gen.path_cpu[:, 1, :]

testval_aseet1_1y = np.abs((np.mean(p1[:, 252]) - 0.99*np.exp(0.02))/(0.99*np.exp(0.02)))
testval_aseet1_2y = np.abs((np.mean(p1[:, -1]) - 0.99*0.99*np.exp(0.04)) / (0.99*0.99*np.exp(0.04)) )

print(testval_aseet1_1y, testval_aseet1_2y)
quanto1y = - quanto2.sigma * quanto2.rho * vol2.sigma
quanto2y = - quanto2.sigma * quanto2.rho * vol2.sigma * 2.0

testval_aseet2_1y = np.abs((np.mean(p2[:, 252]) - spot2.data*np.exp(0.01 + quanto1y)) / (spot2.data*np.exp(0.02 + quanto1y)))
testval_aseet2_2y = np.abs((np.mean(p2[:, -1]) - spot2.data*0.98*np.exp(0.02 + quanto2y)) / (spot2.data*0.98*np.exp(0.04 + quanto2y)))
print(testval_aseet2_1y, testval_aseet2_2y)

x1 = np.log(p1/cp.asnumpy(proc1.cached_forward))
x2 = np.log(p2/cp.asnumpy(proc2.cached_forward))

cov1 = np.cov(x1[:, 252], x2[:, 252])
print(abs(cov1[0, 0] - 0.04)/0.04)
print(abs(cov1[1, 0] - 0.01)/0.01)
print(abs(cov1[1, 1] - 0.01)/0.01)

cov2 = np.cov(x1[:, -1], x2[:, -1])
print(abs(cov2[0, 0] - 0.08)/0.08)
print(abs(cov2[1, 0] - 0.01*2)/(0.01*2))
print(abs(cov2[1, 1] - 0.01*2)/0.01*2)



