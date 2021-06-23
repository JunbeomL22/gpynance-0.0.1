from gpynance import gvar
from gpynance.utils import indexing
# -
import numpy as np
import cupy as cp

import time

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
        #ed = time.time(); print("1-1: ", ed-st)
        self.path_cpu = np.empty((0, self.processes.num_random, self.dtg.number), dtype = self.dtype)

    def cache_cpu_path(self, seed=1):
        self.path_cpu = np.empty((0, self.processes.num_random, self.dtg.number), dtype = self.dtype)

        self.seed = seed
        self.reset_randomstate(seed)
        for step in self.batch_steps:
            #st = time.time()
            add_path = cp.asnumpy(self.simulate_one_batch(step))
            #ed = time.time(); print("2-1: ", ed-st); st = time.time()
            self.path_cpu = np.concatenate((self.path_cpu, add_path), axis=0)
            concatenation takes a lot of time reduce this
            #ed = time.time(); print("2-2: ", ed-st); st = time.time()

    def simulate_one_batch(self, batch = 1):
        bm = self.generate_brownianmotion(batch)
        _, ind = indexing.slicing_brownianmotion(self.processes)
        for i, proc in enumerate(self.processes.processes):
            start = ind[i].start
            end = ind[i].stop
            bm[start:end] = proc.evolve(bm[start:end], self.dtg.times, self.dt)

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
        

