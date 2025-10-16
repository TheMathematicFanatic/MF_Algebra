from ..expressions.numbers.real import Real
import numpy as np


class Infinity(Real):
    def __init__(self, **kwargs):
        super().__init__(np.inf, '\\infty', **kwargs)
inf = Infinity()