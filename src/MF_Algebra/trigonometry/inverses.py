from ..expressions.functions import Function
import numpy as np


arcsin = Function('\\arcsin', 6, np.arcsin)
arccos = Function('\\arccos', 6, np.arccos)
arctan = Function('\\arctan', 6, np.arctan)

arcsec = Function('\\arcsec', 6, lambda x: np.arccos(1/x))
arccsc = Function('\\arccsc', 6, lambda x: np.arcsin(1/x))
arccot = Function('\\arccot', 6, lambda x: np.arctan(1/x))