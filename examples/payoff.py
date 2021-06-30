from gpynance.instruments import condition, payoff, cashflow, payment
from gpynance.engines.montecarlo import path
from gpynance.utils import data, referencedate
from gpynance.parameters import curve, dividend

from examples import pathgen_sample
# -
import QuantLib as ql
import numpy as np
# -
ref_date = pathgen_sample.ref_date
mat = pathgen_sample.mat
dtg = pathgen_sample.dtg

# - get path
p1 = pathgen_sample.p1
sp1 = path.SinglePath(dtg, p1)
p2 = pathgen_sample.p2
sp2 = path.SinglePath(dtg, p2)
multi_path = path.MultiPath(dtg, [sp1, sp2])

# - parameter
risk_free_rate = 0.02
monthly_coupon_amount = risk_free_rate / 12.0
rf_curve = curve.ZeroCurve([1.0], data.Data([risk_free_rate]), ref_date)

# - make els payoffs
# - build dates
coup_dates = [ref_date.date + ql.Period(f"{i}M") for i in range(1, 7)]
red_date = ref_date.date + ql.Period("6M")
lizard_period = [ref_date.date, red_date]
# - build coupon payoff
coup_conditions= [condition.WorstLowerBarrier(d, [1.0, 2.0], 0.6) for d in coup_dates] 
coup_amounts   = [monthly_coupon_amount for i in range(len(coup_conditions))]
coup_payments  = [payment.FixedCoupon(c) for c in coup_amounts]
coup_payoffs = []
for i in range(len(coup_conditions)):
    po = payoff.MaskedPayoff(coup_conditions[i], coup_payments[i], coup_dates[i])
    coup_payoffs.append(po)

