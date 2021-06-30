from gpynance import gvar
from gpynance.utils import myexception
# - 
import numpy as np
import QuantLib as ql

class CashFlowTable:
    def __init__(self, n, dtype = gvar.dtype, name = ""):
        self.n = n
        self.dtype = dtype
        self.name = name
        self.cashflow = np.zeros(self.n, dtype = self.dtype)
        self.redemption_date = np.zeros(self.n, dtype='int32')
        self.not_redemped = np.one(self.n, dtype = bool)

    def add_cashflow(where_met, x, under_redemped = False):
        """
        add_cashflow(where_met, x, under_redemped = False)
        under_redemped == True means that action is taken only for not redemped scenario
        """
        if under_redemped:
            mask = np.copy(self.not_redemped)
            mask[mask] = where_met
            self.cashflow[mask] += x
        else:
            self.cashflow[mask] += x
        
    def set_redemption(date, where_met, x, under_redemped = False):
        if isinstance(date, ql.Date):
            d = date.serialNumber()
        elif isinstance(date, Int):
            d = date
        else:
            raise myexception.MyException(f"set_redemption for {type(date)} has not been defined", self, self.name)

        if under_redemped:
            mask = np.copy(self.not_redemped)
            mask[mask] = where_met
            self.not_redemped[mask] = False
            self.cashflow[mask]  += x
            self.redemption_date[mask] = d
        else:
            self.not_redemped = np.logical_and(where_met, self.not_redemped)
            self.cashflow[self.not_redemped]  += x
            self.redemption_date[self.not_redemped] = d
        
