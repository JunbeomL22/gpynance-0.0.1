from gpynance.processes import process
from gpynance.utils import myexception
# -
import numpy as np

def slicing_brownianmotion(processes):
    count = 0
    slices = []
    dimensions = []

    for proc in processes.processes:
        if isinstance(proc, process.Process1D):
            dimensions += [1]
        elif isinstance(proc, process.Process2D):
            dimensions += [2]
        else:
            raise myexception.MyFunctionException("Only 1d and 2d processes are considerd", "slicing_brownianmotion")
    count  = sum(dimensions)
    if len(dimensions) == 1:
        return count, [slice(0, dimensions[0])]
    idx_ed = np.add.accumulate(dimensions)
    idx_st = [0]
    idx_st = np.append(idx_st, idx_ed[:-1])
    idx = list(map(lambda z: slice(z[0], z[1]), zip(idx_st, idx_ed)))
    return count, idx


#julia equivalence

#function bm_index(pr::Vector{StochasticProcess})
#    count::Int = 0
#    ind = Vector{UnitRange{Int}}[]
#    dimensions = Int[]
#    for p in pr
#        if typeof(p) <: StochasticProcess1D
#            append!(dimensions, 1)
#        elseif typeof(p) <: StochasticProcess2D
#            append!(dimensions, 2)
#        end
#    end #(1d, 2d, 1d) => [1, 2, 1]
#    count = sum(dimensions)
#    idx_ed = accumulate(+, dimensions)
#    idx_st = [1]
#    append!(idx_st, idx_ed[1:end-1] .+ 1)
#    ind = map(x->x[1]:x[2], zip(idx_st, idx_ed))
#    return count, ind
#end

