from gpynance import gvar
from gpynance.utils import indexing
# -
import numpy as np
import cupy as cp

import threading

class GpuPathGenerator:
    def __init__(self, dtg, processes, num_simulation = 1, seed = 1, dtype = gvar.dtype, batch_size = None):
        self.seed = seed
        self.dtype = dtype
        self.processes = processes
        self.dtg = dtg

        self.num_simulation = num_simulation
        self.randomstate = cp.random.RandomState(self.seed, cp.cuda.curand.CURAND_RNG_PSEUDO_MT19937)
        self.num_random = self.processes.num_random
        
        self.batch_size = min(batch_size, num_simulation) if batch_size is not None else self.num_simulation
        self.make_batch_steps(self.batch_size) # when num_sim = 203 and batch = 100, we have self.batch_steps = [100, 100, 3]

        #st = time.time()
        self.times = cp.array(dtg.times, dtype = self.dtype)
        self.dt = cp.array(dtg.dt, dtype = self.dtype)
        self.sqdt = cp.sqrt(self.dt)
        
        self.path_cpu = np.empty((self.num_simulation, self.processes.num_random, self.dtg.number), dtype = self.dtype)

    def cache_cpu_path(self, seed=None):
        """
        The majority of calculation cost occurs in (the number is rough estimation) 
        (1) random state initialization: 12 %
        (2) gpu -> cpu transfer: 70 %
        (3) insertion to numpy array: 18 %

        NOTE that the path calculation take time ZERO.
        Therefore, computational power of gpu does not matter AT ALL.
        The crucual part is (2), i.e., the performance of PCI lane dominates the majority of computation time.
        
        The time in (1) occurs becauese cupy compile at the beginning. 
        To reduce (3), you may want to use thread. 
        But the proformance improvement by threading would be marginal (I guess), or even slower.

        For now, the gpu -> cpu transfer and insertion are implemented in threading.
        Check later if the threading improves the performance.
        """
        for _, proc in enumerate(self.processes.processes):
            proc.cache(self.dtg)

        def _insertion(_x, _y, _slice):
            _x[_slice.start:_slice.stop] = cp.asnumpy(_y)
        
        slice_stop = 0
        thread = []
        for step in self.batch_steps:
            # _path_gpu = self.simulate_one_batch(step)
            thread.append(threading.Thread(target=_insertion,
                                           args=(self.path_cpu, self.simulate_one_batch(step), slice(slice_stop, slice_stop+step))))
            #self.path_cpu[slice_stop:slice_stop + step] = cp.asnumpy(_path_gpu)
            slice_stop += step
       
        for t in thread:
            t.start()
            
        for t in thread:
            t.join()

        print("(pathgenerator.cache_cpu_path) For now, the gpu -> cpu transfer and insertion are implemented in threading.")
        print("Check later if the threading improves the performance.\n")
            

    def simulate_one_batch(self, batch = 1):
        bm = self.generate_brownianmotion(batch)
        _, ind = indexing.slicing_brownianmotion(self.processes)
        for i, proc in enumerate(self.processes.processes):
            start = ind[i].start
            end = ind[i].stop
            bm[:, start:end, :] = proc.evolve(bm[:, start:end, :], self.dtg.times, self.dt)

        return bm

    def generate_brownianmotion(self, num = 1):
        mean = cp.zeros(self.num_random, dtype = self.dtype)  # obviously zero by the definition of BM
        corr = self.processes.corr
        num_timestep = self.dtg.number
        
        bm = self.randomstate.multivariate_normal(mean, corr, (num, num_timestep), method = 'cholesky', dtype = self.dtype)
        bm = cp.transpose(bm, (0, 2, 1)) * self.sqdt

        return bm
        
    def reset_randomstate(self, seed = 1):
        self.seed = 1
        self.randomstate = cp.random.RandomState(self.seed, cp.cuda.curand.CURAND_RNG_PSEUDO_MT19937)

    def make_batch_steps(self, n):
        num = self.num_simulation // n
        residual = self.num_simulation % n

        res = [n] * num
        if residual == 0:
            self.batch_steps = res
        else:
            self.batch_steps = res + [residual]
        

