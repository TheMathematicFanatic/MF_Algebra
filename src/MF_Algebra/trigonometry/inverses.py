from ..expressions.functions import Function
import math


arcsin = Function('\\arcsin', 6, math.asin)
arccos = Function('\\arccos', 6, math.acos)
arctan = Function('\\arctan', 6, math.atan)

arcsec = Function('\\arcsec', 6, lambda x: math.acos(1/x))
arccsc = Function('\\arccsc', 6, lambda x: math.asin(1/x))
arccot = Function('\\arccot', 6, lambda x: math.atan(1/x))