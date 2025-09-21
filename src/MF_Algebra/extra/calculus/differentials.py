from ...expressions.functions.functions import Function
from ...expressions.variables import x, y, z, r, theta, s, t, u, v


class DifferentialOperator(Function):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


d = DifferentialOperator(
	symbol = "\\mathrm{d}",
	symbol_glyph_length = 1,
	parentheses_mode="weak",
)

dx = d(x)
dy = d(y)
dz = d(z)
dr = d(r)
dtheta = d(theta)
ds = d(s)
dt = d(t)
du = d(u)
dv = d(v)


def dd(var):
    return d/d(var)
