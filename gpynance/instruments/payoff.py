from gpynance.instruments import cashflow

class MaskedPayoff:
    """
    get_mask_and_cash method returns the mask and the payment ON the mask
    For example, if the output mask is [True, False, True], then the length of output pay is 2
    """
    def __init__(self, condition, payment, payment_date):
        self.condition = condition
        self.payment = payment
        self.payment_date = payment_date

    def get_mask_and_cash(self, multi_path, mask=None): 
        """
        get_mask_and_cash(self, multi_path, mask=None)

        This returns like mask = [True, False, False, True], pay = [0.01, 0.01]
        """
        met = self.condition(multi_path, mask)
        pay = self.payment(multi_path, met)
        return met, pay

class ElsRedemptionPayoff:
    def __init__(self, redemption, monthly_coupon, path_barrier_payoff = None, knockin_payoff = None):
        """
        All Payoffs are MaskedPayoff
        """
        self.redemption = redemption
        self.monthly_coupon = monthly_coupon
        self.path_barrier_payoff = path_barrier_payoff
        self.knockin_payoff = knockin_payoff
        
    def set_cashflow(self, cashflowtable, multi_path, discount_curve, masking_ratio = 0.1):
        """
        set_cashflow(cashflowtable, multi_path, discount_curve, masking_ratio=1.0)

        masking_ratio is a criterion for masking condition.
        For example, the remaining path not redemped until maturity is under 10% (=masking_ratio)
        the path barrier check is under the masked path.
        """
        not_redemped = cashflowtable.not_redemped
        
        for coupon in self.monthly_coupon:
            # e.g., mask_c = [True, False, False, True], pay_c = [0.01, 0.01]
            met_c, pay_c = coupon.get_mask_and_cash(multi_path)
            pay_c *= discount_curve.discount(coupon.payment_date)
            cashflowtable.add_cashflow(met_c, pay_c)
        # check range
        met_redem, pay_redem = self.redemption.get_mask_and_cash(multi_path)
        pay_redem *= discount_curve.discount(self.redemption.payment_date)
        cashflowtable.set_redemption(self.redemption.payment_date, met_redem, pay_redem)
        
        # check path_barrier
        if (self.path_barrier_payoff is None) or (len(self.path_barrier_payoff) == 0):
            return None
        
        not_redemped = cashflowtable.not_redemped
        if np.sum(not_redemped) / not_redemped.shape[0] < masking_ratio:
            met_lz, pay_lz = self.path_barrier_payoff.get_mask_and_cash(multi_path, not_redemped)
            pay_lz *= discount_curve.discount(self.path_barrier_payoff.payment_date)
            cashflowtable.set_redemption(self.redemption.payment_date, met_lz, pay_lz, under_redemped = True)
        else:
            met_lz, pay_lz = self.path_barrier_payoff.get_mask_and_cash(multi_path)
            pay_lz *= discount_curve.discount(self.path_barrier_payoff.payment_date)
            cashflowtable.set_redemption(self.redemption.payment_date, met_lz, pay_lz, under_redemped = False)

        # is there a knockin? 
        if (self.knockin_payoff is None) or (len(self.knockin_payoff) == 0):
            return None
        # The following highly likely has changed after checking path_barrier redemption (or maturity)
        not_redemped = cashflowtable.not_redemped 
        _, pay_ki = self.knockin_payoff.get_mask_and_cash(multi_path, not_redemped)
        pay_ki *= discount_curve.discount(self.knockin_payoff.payment_date)
        cashflowtable.cashflow[not_redemped] = pay_ki
        cashflowtable.redemption_date[not_redemped] = self.knockin_payoff.payment_date
        
class CallableFloaterPayoff:
    def __init__(self, schedules, spread=0.0):
        self.schedules = schedules # (fixing, start, end, pay)
        self.spread = spread

    def set_swapcashflow(self, swap_cft, redemption_date, index, discount_curve):
        swap_payments = []
        for sc in schedules:
            if sc.payment_date < multi_path.dtg.ref_date.date:
                continue
            d = sc.payment_date
            p = (index.fixing(sc.fixing) + self.spread)
            p *= index.dc.yearFraction(sc.calc_start, calc_end)
            p *= discount_curve.discount(d)
            swap_payments.append((d, p))

        for i, dp in enumerate(swap_payments):
            cond = dp[0].serialNumber() <= redemption_date
            swap_cft.add_cashflow(cond, dp[1])
            

"""
class Payoff:
    
    get_mask_and_cash method returns the mask and the payment ON the mask
    For example, if the output mask is [True, False, True], then the length of output pay is 2
    
    def __init__(self, condition, payment_met, payment_notmet, payment_date):
        self.condition = condition
        self.payment = payment
        self.payment_date = payment_date
        self.payment_notmet = payment_notmet

    def get_mask_and_cash(self, multi_path, mask=None):
    
        This returns like mask = [True, False, False, True], pay = [0.01, 0.01]
    
        met = self.condition(multi_path, mask)
        notmet = np.logical_not(met)
        pay_met = self.payment_met(multi_path, met)
        pay_notmet = self.payment_notmet(multi_path, notmet)
        res = np.zeros(met.shape[0], dtype=multi_path.single_paths[0].dtype)
        res[met] = pay_met
        res[notmet] = pay_notmet
        return met, res
"""
