from numba import cuda
import cupy as cp

@cuda.jit(device=True, inline=True)
def step_evolve(lv, dt, z):
    """
    step_evolve(vol_fx, corr_fx, lv, dt, z)
    float(float, float,  float)
    z = dw ->  - σ^FX * ρ^FX dt - 0.5*lv^2*dt +lv*z 
    return init + lv*z - 0.5*lv^2dt
    """
    return - (0.5*lv*lv)*dt + (lv*z)
        
@cuda.jit
def set_path(res_mat, dt, vol_xgrid, vol_surface, vol_derivative, extrapolate=False):
    """
    set_multiasset_multipath(res_mat, dt, vol_fx, corr_fx, vol_xgrid, vol_surface, vol_derivative, extrapolate=False)
    float[:,:,:], float[:], float[:, :,:], float[:, :,:], float[:, :,:], bool
    Note that the input variable res is a brownian_motion of simNum * assetNum * dateNum
    """
    n = cuda.grid(1)
    if n < res_mat.shape[0]:
        res = res_mat[n]
        assetNum = res.shape[0]
        dateNum  = res.shape[1]
        for i in range(assetNum):
            res[i][0] = 0.0
            for t in range(1, dateNum):
                prev_val = res[i][t-1]
                z = res[i][t]
                vol = interp_value_at(t-1, prev_val, vol_xgrid[i], vol_surface[i], vol_derivative[i], extrapolate)
                res[i][t] = prev_val + step_evolve(vol, dt[t], z)

@cuda.jit
def set_ith_asset(i, res_mat, dt, vol_xgrid, vol_surface, vol_derivative, extrapolate=False):
    """
    set_multiasset_multipath(res_mat, dt, vol_fx, corr_fx, vol_xgrid, vol_surface, vol_derivative, extrapolate=False)
    i: int, res_mat: float[:,:,:], dt: float[:], vol_xgrid: float[:,:], 
    vol_surface: float[:,:], vol_derivative: float[:,:], extrapolate: bool
    Note that the input variable res is a brownian_motion of simNum * assetNum * dateNum
    """
    n = cuda.grid(1)
    if n < res_mat.shape[0]:
        res = res_mat[n]
        dateNum  = res.shape[1]
        
        res[i][0] = 0.0
        for t in range(1, dateNum):
            prev_val = res[i][t-1]
            z = res[i][t]
            vol = interp_value_at(t-1, prev_val, vol_xgrid, vol_surface, vol_derivative, extrapolate)
            res[i][t] = prev_val + step_evolve(vol, dt[t], z)
                
@cuda.jit(device=True)
def interp_value_at(i, x_val, x_mat, y_mat, deriva_mat, extrapolate=False):
    """
    interp_value(x_val, x_vec, y_vec, deriva, extrapolate)
    float(int, float, float[:], float[:,:], float[:,:], bool)
    """
    return interp_value(x_val, x_mat[i], y_mat[i], deriva_mat[i], extrapolate)

@cuda.jit(device=True)
def interp_value(x_val, x_vec, y_vec, deriva_vec, extrapolate=False):
    """
    interp_value(x_val, x_vec, y_vec, deriva, extrapolate)
    float(float, float[:,:], float[:,:], float[:,:], bool)
    """
    res=0.0
    if x_val <= x_vec[0]:
        if extrapolate:
            res = y_vec[0] + deriva_vec[0]* (x_val-x_vec[0])
        else:
            res = y_vec[0]
    elif x_val > x_vec[-1]:
        if extrapolate:
            res = y_vec[-1] + deriva_vec[-1]* (x_val-x_vec[-1])
        else:
            res = y_vec[-1]
    else:
        idx=-1
        for i, x in enumerate(x_vec):
            if x < x_val and x_val <= x_vec[i+1]:
                idx = i
                break
        
        res = y_vec[idx] + deriva_vec[idx]* (x_val-x_vec[idx])

    return res
