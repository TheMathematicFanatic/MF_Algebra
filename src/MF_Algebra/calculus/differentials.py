from ..expressions.functions.functions import Function, arg
from ..expressions.variables import x, y, z, r, theta, s, t, u, v
from ..expressions.combiners.operations import Div


class DifferentialOperator(Function):
	pass


d = DifferentialOperator(
	symbol = '\\mathrm{d}',
	symbol_glyph_length = 1,
	parentheses_mode = 'weak'
)
delta = DifferentialOperator(
	symbol = '\\mathrm{\\delta}',
	symbol_glyph_length = 1,
	parentheses_mode = 'weak'
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


class DifferentialQuotientOperator(DifferentialOperator, Div):
	d_op = d
	def __init__(self, var, **kwargs):
		super().__init__(self.d_op, self.d_op(var), **kwargs)

def dd(var):
    return DifferentialQuotientOperator(var)


class PrimeOperator(DifferentialOperator):
	string_code = [arg, '^\\prime']
	glyph_code = [arg, 1]
prime = PrimeOperator()
