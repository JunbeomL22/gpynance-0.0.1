import numpy as np

class WorstPerformer:
    def __call__(self, x):
        return np.amin(x, axis=1)

class BestPerformer:
    def __call__(self, x):
        return np.amax(x, axis=1)

class AveragePerformer:
    def __call__(self, x):
        return np.mean(x, axis=1)
