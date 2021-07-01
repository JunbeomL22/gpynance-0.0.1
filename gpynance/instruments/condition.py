import numpy as np
from gpynance import gvar

class Unconditional:
    def __init__(self):
        pass

    def __call__(self, multi_path, mask = None):
        """
        x = list of numpy arrays
        If you really want to tighten performance, use numba aot
        """
        num_sim = multi_path.single_paths[0].path.shape[0]
        if mask is not None:
            num_sim = np.sum(mask)
        
        return np.ones(num_sim, dtype='bool')
    
class WorstLowerBarrier:
    def __init__(self, date, base_price, barrier_ratio, dtype = gvar.dtype):
        self.date = date
        self.base_price = base_price
        self.barrier_ratio = barrier_ratio
        self.dtype = dtype
        self.barrier = np.array(self.base_price, dtype = dtype) * barrier_ratio

    def __call__(self, multi_path, mask = None):
        """
        x = list of numpy arrays
        If you really want to tighten performance, use numba aot
        """
        x = multi_path(self.date, mask = mask)
        res = x[0] >= self.barrier[0]
        n = len(x)
        if n == 1:
            return res
        for i in range(1, n):
            res = np.logical_and(res, x[i] >= self.barrier[i])
        return res.flatten()

class WorstMeanLowerBarrier(WorstLowerBarrier):
    def __init__(self, date, num, base_price, barrier_ratio, dtype = gvar.dtype):
        super().__init__(date, base_price, barrier_ratio, dtype = gvar.dtype)
        self.num = num
    def __call__(self, multi_path, mask=None):
        """
        x = list of numpy arrays
        If you really want to tighten performance, use numba aot
        """
        z = []
        x = multi_path(self.date, num = self.num, mask = mask)
        for e in x:
            z.append(np.mean(e, axis=1))
        return super().__call__(z)
    
class PathWorstLowerBarrier:
    def __init__(self, start_date, end_date, base_price, barrier_ratio, is_past_hit, dtype = gvar.dtype):
        self.start_date = start_date
        self.end_date = end_date
        self.base_price = base_price
        self.barrier_ratio = barrier_ratio
        self.dtype = dtype
        self.barrier = np.array(self.base_price, dtype = dtype) * barrier_ratio
        self.is_past_hit = is_past_hit

    def __call__(self, multi_path, mask = None):
        x = multi_path(start_date = self.start_date, end_date = self.end_date, mask = mask)
        
        if self.is_past_hit:
            return np.zeros(x[0].shape[0], dtype = bool)
        
        mask = np.all(x[0] >= self.barrier[0], axis = 1)
        n = len(x)
        if n == 1:
            return mask
        for i in range(1, n):
            mask = np.logical_and(mask, np.all(x[i] >= self.barrier[i], axis=1))
            
        return mask.flatten()
