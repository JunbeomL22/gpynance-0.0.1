import numpy as np

class LowerBarrier:
    def __init__(self, barrier):
        self.barrier = barrier

    def __call__(self, x):
        return x >= self.barrier

class LowerPathBarrier:
    def __init__(self, barrier, xp = np):
        self.xp = xp
        self.barrier = barrier

    def __call__(self, x):
        return self.xp.all(x >= self.barrier, axis=1)

class UpperBarrier:
    def __init__(self, barrier):
        self.barrier = barrier

    def __call__(self, x):
        return x < self.barrier

class UpperPathBarrier:
    def __init__(self, barrier, xp = np):
        self.xp = xp
        self.barrier = barrier

    def __call__(self, x):
        return self.xp.all(x < self.barrier, axis=1)
