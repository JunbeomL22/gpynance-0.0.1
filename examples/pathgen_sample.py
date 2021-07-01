from gpynance.utils import referencedate, data, datetimegrid
from gpynance.parameters import curve, dividend, volatility
from gpynance.engines.montecarlo import path, pathgenerator
from gpynance.processes import gbm, process
from gpynance import null_parameter
# -
import QuantLib as ql
import numpy as np
import cupy as cp

import time

# - time setup
_mat = "2Y"
ref_date = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
mat = ref_date + ql.Period(_mat)
dtg = datetimegrid.DateTimeGrid(ref_date, mat)

# - initial value. Note that these are observable
spot1 = data.Data(1.0)
spot2 = data.Data(1.0)

# - volatility setup, not observable
vol1 = volatility.ConstantVolatility(sigma=0.2, name = "asset1's vol")
quanto1 = volatility.Quanto(sigma = 0.0, rho = 0.0, name = "asset1's quanto (no quanto)")

vol2 = volatility.ConstantVolatility(sigma = 0.1, name = "asset2's vol")
quanto2 = volatility.Quanto(sigma = 0.02, rho = -0.1, name = "asset1's quanto")

corr = cp.identity(2)
corr[0, 1] = corr[1, 0] = 0.5

# - risk_free and dividend, see how they work with Data class. Recall that Data class is observable
risk_free_data1 = data.Data([0.02])
risk_free_data2 = data.Data([0.01])

risk_free1 = curve.ZeroCurve([dtg.times[-1]], risk_free_data1, ref_date)
risk_free2 = curve.ZeroCurve([dtg.times[-1]], risk_free_data2, ref_date)

div_dates1 = [ref_date + ql.Period("1D"), ref_date + ql.Period("2Y")]
div_dates2 = [ref_date + ql.Period("2D"), ref_date + ql.Period("2Y")]
dividend_data1 = data.Data([0.01, 0.01])
dividend_data2 = data.Data([0.0,  0.02])

dividend1 = dividend.Dividend(div_dates1, dividend_data1, ref_date)
dividend2 = dividend.Dividend(div_dates2, dividend_data2, ref_date)

null_curve = null_parameter.null_yts

# - build processes
proc1 = gbm.GbmProcess(spot1, vol1, quanto1, risk_free1, dividend1)
proc2 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
processes = process.Processes([proc1, proc2], corr)

# - generating path
sim = 100000
batch = 25000
gen = pathgenerator.GpuPathGenerator(dtg, processes, num_simulation = sim, seed = 1, batch_size = batch)
gen.cache_cpu_path()
p1 = gen.path_cpu[:, 0, :]
p2 = gen.path_cpu[:, 1, :]
sp1 = path.SinglePath(dtg, p1)
sp2 = path.SinglePath(dtg, p2)
multi_path = path.MultiPath(dtg, [sp1, sp2])
