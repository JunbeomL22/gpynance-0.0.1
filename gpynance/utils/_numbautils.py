from numba.pycc import CC
import numpy as np

cc = CC('numbautils')

@cc.export('indexi4', '(i4[:], i4)')
@cc.export('indexi8', '(i8[:], i8)')
@cc.export('indexf4', '(f4[:], f4)')
@cc.export('indexf8', '(f8[:], f8)')
def index(array, item):
    n = len(array)
    for i in range(n):
        if abs(array[i]-item) < 1.0e-16:
            return i
        
    return -1

@cc.export('sortedindexf4', '(f4[:], f4)')
@cc.export('sortedindexf8', '(f8[:], f8)')
def sortedindex(array, item):
    """
    ex) 
    arr = np.array([1.0, 2.0, 3.0], dtype='float32')
    sortedindex(arr, 0.5) => (0, 1.0)
    sortedindex(arr, 1.2) => (0, 0.8)
    sortedindex(arr, 3.5) => (-1, 1.0)
    """
    if item < array[0]:
        return 0, 1.0
    
    if item >= array[-1]:
        return -1, 1.0

    n = len(array)
    for idx in range(n-1):
        if item >= array[idx] and item < array[idx+1]:
            return idx, (1.0 - (item-array[idx]))
        
#cc.compile()
