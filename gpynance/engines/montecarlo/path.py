from gpynance.utils import myexception, numbautils
#-
import QuantLib as ql
import numpy as np

class SinglePath:
    """
    SinglePath(dtg, path, past = {}, name = "", xp = np)
    __call__ method has been implemented to get and slice path and past val
    For use cases, run gpynance/examples/path.py and see the results
    There are a lot of hacks in __call__. Please improve this.
    """
    def __init__(self, dtg, path, past = {}, name = "", xp = np):
        self.dtg = dtg
        self.path = path
        self.past = past # dict type. this may be improved to be another Path Type
        self.name = name
        self.xp = xp

    def slicing(self, st, ed, mask, after_ref):
        if ed > self.dtg.dates[-1]:
            raise myexception.MyException("end date for slicing is bigger than datetimegrid", self, self.name)
        
        ed_idx, _ = numbautils.sortedindexi4(self.dtg.serialnumber, ed.serialNumber())
        
        if after_ref:
            st = max(st, self.dtg.ref_date.date)
            st_idx, _ = numbautils.sortedindexi4(self.dtg.serialnumber, st.serialNumber())
        else:
            if st < self.dtg.ref_date:
                st_idx = 0
            else:
                st_idx, _ = numbautils.sortedindexi4(self.dtg.serialnumber, st.serialNumber())

        if mask is None:
            res = self.path[:, st_idx:ed_idx]
            num_path = self.path.shape[0]
        else:
            res = self.path[mask][:, st_idx:ed_idx]
            num_path = np.sum(mask)

        if st >= self.dtg.ref_date.date:
            return res
        
        x = [self.past[k] for k in sorted(self.past) if k >= st]
        past_vals = self.xp.array(x, dtype = self.path.dtype)

        con = np.tile(past_vals, (num_path, 1))
        
        return np.concatenate((con, res), axis=1)
        
    def __call__(self, d=None, num = 1, mask = None, start_date=None, end_date=None, after_ref = True):
        """
        getitem returns the value of path at d (the type must ql.Date)
        if d (input) < self.dtg.ref_date.date, this returns the closest history value
        """
        if isinstance(start_date, ql.Date) and isinstance(end_date, ql.Date) and (d is None):
            return self.slicing(start_date, end_date, mask, after_ref)

        if d is None:
            raise myexception.MyException(f"d is not Date type", self, self.name)
        
        idx, _ = numbautils.sortedindexi4(self.dtg.serialnumber, d.serialNumber())
        
        start = max(idx - num + 1, 0)
        end = min(idx+1, len(self.dtg.dates))
        past_num = max(num -1 -idx, 0)
        
        if mask is None:
            num_path = self.path.shape[0]
        else:
            num_path = np.sum(mask)
                
        if idx == -1:
            if d >= self.dtg.ref_date:
                error = f"{d} > {self.ref_date.date} \n"
                error += f"but there is no simulated path data at {d}"
                raise myexception.MyException(error, self, self.name)
            else:
                if num == 1:
                    return self.xp.tile(self.get_past(d), (num_path, 1))
                else:
                    res = self.xp.empty((num_path, 0))
        else:
            if mask is None:
                res = self.path[:, start:end]
            else:
                res = self.path[mask][:, start:end]
        
        if past_num != 0:
            calendar = self.dtg.calendar
            day = calendar.adjust(self.dtg.ref_date.date - ql.Period("1D"), ql.Preceding)
            x = self.get_past(day)
            past_vals = self.xp.array(x, dtype = self.path.dtype)
            
            for i in range(past_num-1):
                day = calendar.adjust(day - ql.Period("1D"), ql.Preceding)
                x = self.get_past(day)
                x = self.xp.array(x, dtype = self.path.dtype)
                past_vals = self.xp.concatenate((x, past_vals), axis=1)

            past_vals = self.xp.tile(past_vals, (num_path, 1))
            res = self.xp.concatenate((past_vals, res), axis=1)
            
        return res
            
    def get_past(self, d):
        """
        If there is no past value in the date, it returns the value at the evaluation date.
        This should be improved later.
        This return e.g., [[[1.0], [2.0], [3.0]]]
        """
        ret=[[self.past.get(d, self.path[0][0])]]

        return ret

    def clone_upto(self, slice_end):
        if not isinstance(slice_end, ql.Date):
            raise myexception.MyException("The clone method for path has been implemented only for ql.Date type", self, self.name)
        
        _dtg = self.dtg.clone_upto(slice_end)
        path_length = _dtg.times.shape[0]
        _path = SinglePath(_dtg, self.path[:, :path_length], past = self.past, xp=self.xp, name = self.name)
        return _path

class MultiPath:
    """
    SinglePath(dtg, path, past = {}, name = "", xp = np)
    __call__ method has been implemented to get and slice path and past vals
    For use cases, run gpynance/examples/path.py and see the results
    There are a lot of hacks in __call__. This should be modified later
    """
    def __init__(self, dtg, single_paths=[], name = "", xp = np):
        self.dtg = dtg
        self.single_paths = single_paths 
        
    def __call__(self, d=None, num = 1, mask = None, start_date=None, end_date=None, after_ref = True):
        ret = []
        for i, p in enumerate(self.single_paths):
            ret.append(p(d, num, mask, start_date, end_date, after_ref))
            
        return ret
    
    def clone_upto(self, slice_end):
        if not isinstance(slice_end, ql.Date):
            raise myexception.MyException("The clone method for path has been implemented only for ql.Date type", self, self.name)
        
        _dtg = self.dtg.clone_upto(slice_end)
        _path=[]
        for i, p in enumerate(self.single_paths):
            path.append(p.clone_upto(slice_end))
        _multipath =  MultiPath(_dtg, _path)
        return _multipath
    
class Path:
    """
    Path(dtg, path, past = {}, name = "", xp = np)
    
    __call__ method has been implemented to get and slice path and past vals

    For use cases, run gpynance/examples/path.py and see the results
    
    There are a lot of hacks in __call__. This should be modified later
    """
    def __init__(self, dtg, path, past = {}, name = "", xp = np):
        self.dtg = dtg
        self.path = path
        self.past = past # [{Date => 0.1, Date => ...}] each element is dict # may be improved to be another Path Type
        self.name = name
        self.xp = xp
        
    def __call__(self, d, num = 1, mask = None):
        """
        getitem returns the value of path at d (the type must ql.Date)
        if d (input) < self.dtg.ref_date.date, this returns the closest history value
        """
        if not isinstance(d, ql.Date):
            raise myexception.MyException("The input type for path slicing must be ql.Date", self, self.name)

        idx, _ = numbautils.sortedindexi4(self.dtg.serialnumber, d.serialNumber())

        start = max(idx - num + 1, 0)
        end = min(idx+1, len(self.dtg.dates))
        past_num = max(num -1 -idx, 0)
        
        if mask is None:
            num_path = self.path.shape[0]
        else:
            num_path = np.sum(mask)
                
        if idx == -1:
            if d >= self.dtg.ref_date:
                error = f"{d} > {self.ref_date.date} \n"
                error += f"but there is no simulated path data at {d}"
                raise myexception.MyException(error, self, self.name)
            else:
                if num == 1:
                    return self.xp.tile(self.get_past(d), (num_path, 1, 1))
                else:
                    res = self.xp.empty((num_path, self.path.shape[1], 0))
        else:
            if mask is None:
                res = self.path[:, :, start:end]
            else:
                res = self.path[mask][:, :, start:end]
        
        if past_num != 0:
            calendar = self.dtg.calendar
            day = calendar.adjust(self.dtg.ref_date.date - ql.Period("1D"), ql.Preceding)
            x = self.get_past(day)
            past_vals = self.xp.array(x, dtype = self.path.dtype)
            
            for i in range(past_num-1):
                day = calendar.adjust(day - ql.Period("1D"), ql.Preceding)
                x = self.get_past(day)
                x = self.xp.array(x, dtype = self.path.dtype)
                self.xp.concatenate((x, past_vals), axis=2)

            past_vals = self.xp.tile(past_vals, (num_path, 1, 1))
            res = self.xp.concatenate((past_vals, res), axis=2)
            
        return res
            

    def get_past(self, d):
        """
        If there is no past value in the date, it returns the value at the evaluation date.
        This should be improved later.
        
        This return e.g., [[[1.0], [2.0], [3.0]]]
        """
        ret = []
        for i, v in enumerate(self.past):
            ret.append([v.get(d, self.path[0][i][0])])

        return [ret]

    def clone_upto(self, slice_end):
        if not isinstance(slice_end, ql.Date):
            raise myexception.MyException("The clone method for path has been implemented only for ql.Date type", self, self.name)
        
        _dtg = self.dtg.clone_upto(slice_end)
        path_length = _dtg.times.shape[0]
        _path = Path(_dtg, self.path[:, :, :path_length], past = self.past, xp=self.xp, name = self.name)
        return _path
