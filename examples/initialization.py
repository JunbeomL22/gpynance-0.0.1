import threading

def non_thread(_n, _x, _slices, _addition):
    for i in range(_n):
        _x[_slices[i]] = _addition[i]

def ith_insertion(_i, _n, _x, _slices, _addition):
    _x[_slices[_i]] = _addition[_i]
        
def use_thread(_n, _x, _slices, _addition):
    thread = []
    for _i in range(_n):
        thread.append(threading.Thread(target=ith_insertion, args=(_i, _n, _x, _slices, _addition)))
   
    for _i in range(_n):
        thread[_i].start()

    for _i in range(_n):
        thread[_i].join()


