from gpynance.processes import process, gbm
from gpynance.parameters import volatility, curve, dividend
from gpynance.engines.montecarlo import path, pathgenerator
from gpynance.utils import referencedate, datetimegrid, data, indexing
from gpynance import gvar, null_parameter
# -
import QuantLib as ql
import numpy as np
import cupy as cp

import time

def make_path_gen(sim, batch, mat):
    # - time setup
    ref_date = referencedate.ReferenceDate(ql.Date(4, 1, 2021))
    mat = ref_date + ql.Period(mat)
    dtg = datetimegrid.DateTimeGrid(ref_date, mat)
    
    # - initial value
    spot1 = data.Data(1.0)
    spot2 = data.Data(2.0)
    
    # - volatility setup
    vol1 = volatility.ConstantVolatility(sigma=0.2, name = "asset1's vol")
    quanto1 = volatility.Quanto(sigma = 0.0, rho = 0.0, name = "asset1's quanto (no quanto)")

    vol2 = volatility.ConstantVolatility(sigma = 0.1, name = "asset2's vol")
    quanto2 = volatility.Quanto(sigma = 0.02, rho = -0.1, name = "asset1's quanto")

    corr = cp.identity(2)
    corr[0, 1] = corr[1, 0] = 0.5
    #corr[0, 2] = corr[2, 0] = 0.5
    
    # - risk_free and dividend, see how they work with Data class. Recall that Data class is observable
    risk_free_data1 = data.Data([0.02])
    risk_free_data2 = data.Data([0.01])
    
    risk_free1 = curve.ZeroCurve([3.0], risk_free_data1, ref_date)
    risk_free2 = curve.ZeroCurve([3.0], risk_free_data2, ref_date)
    
    div_dates1 = [ref_date + ql.Period("1Y"), ref_date + ql.Period("2Y")]
    div_dates2 = [ref_date + ql.Period("1Y"), ref_date + ql.Period("2Y")]
    dividend_data1 = data.Data([0.0, 0.0])
    dividend_data2 = data.Data([0.02, 0.02])
    
    dividend1 = dividend.Dividend(div_dates1, dividend_data1, ref_date)
    dividend2 = dividend.Dividend(div_dates2, dividend_data2, ref_date)
    null_curve = null_parameter.null_yts
    
    # - build processes
    proc1 = gbm.GbmProcess(spot1, vol1, quanto1, risk_free1, dividend1)
    proc2 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
    proc3 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
    proc4 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
    proc5 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
    proc6 = gbm.GbmProcess(spot2, vol2, quanto2, risk_free2, dividend2)
    
    processes = process.Processes([proc1, proc2], corr)
    
    # - generating path
    gen = pathgenerator.GpuPathGenerator(dtg, processes, num_simulation = sim, seed = 1, batch_size = batch)
    return gen

gen = make_path_gen(200000, 25000, "2Y")
gen.cache_cpu_path()
p = gen.path_cpu[:, 0, :]
