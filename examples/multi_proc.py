from examples import initialization
import numpy as np
import threading
import multiprocessing
import time


length = 500000000
step = 125000000
x = np.empty(length, dtype = 'float32')
n = length // step
slices = []
addition = []
for i in range(n):
    slices.append(slice(i*step, (i+1)*step))
    addition.append(np.empty(step, 'float32'))

def use_process(_n, _x, _slices, _addition):
    processes = []
    for _i in range(_n):
        processes.append(multiprocessing.Process(target=initialization.ith_insertion, args=(_i, _n, _x, _slices, _addition)))
   
    for _i in range(_n):
        processes[_i].start()

    for _i in range(_n):
        processes[_i].join()


if __name__== "__main__":
    st = time.time()
    initialization.non_thread(n, x, slices, addition)
    print("no thread: ", time.time()-st); st = time.time()
    initialization.use_thread(n, x, slices, addition)
    print("multithread: ", time.time()-st); st = time.time()
    


# %timeit initialization.non_thread(n, x, slices, addition)
# %timeit initialization.use_thread(n, x, slices, addition)
# %timeit use_process(n, x, slices, addition)

