class IborSwapSchedule:
    def __init__(self, fixing, calc_start, calc_end, payment_date):
        self.fixing = fixing
        self.calc_start = calc_start
        self.calc_end = calc_end
        self.payment_date = payment_date
