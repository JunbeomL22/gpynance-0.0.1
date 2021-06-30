import numpy as np
import cupy as cp
import QuantLib as ql
from gpynance.utils import referencedate

dtype = 'float32'
xp = cp
base_calendar = ql.SouthKorea() # this is basically for simulation. Using joint calendar is not much beneficial

