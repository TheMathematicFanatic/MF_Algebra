from .expression_core import *


class Variable(Expression):
	def __init__(self, symbol, symbol_glyph_length=None, **kwargs):
		super().__init__(**kwargs)
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return self.symbol_glyph_length

	@Expression.parenthesize_latex
	def __str__(self):
		return self.symbol

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")


a = Variable('a', 1)
b = Variable('b', 1)
c = Variable('c', 1)

k = Variable('k', 1)
m = Variable('m', 1)
n = Variable('n', 1)

p = Variable('p', 1)
q = Variable('q', 1)
r = Variable('r', 1)

t = Variable('t', 1)
u = Variable('u', 1)
v = Variable('v', 1)

x = Variable('x', 1)
y = Variable('y', 1)
z = Variable('z', 1)

alpha = Variable('\\alpha', 1)
beta = Variable('\\beta', 1)
gamma = Variable('\\gamma', 1)
theta = Variable('\\theta', 1)
phi = Variable('\\phi', 1)

x1 = Variable('x_1', 2)
x2 = Variable('x_2', 2)
x3 = Variable('x_3', 2)
y1 = Variable('y_1', 2)
y2 = Variable('y_2', 2)
y3 = Variable('y_3', 2)
z1 = Variable('z_1', 2)
z2 = Variable('z_2', 2)
z3 = Variable('z_3', 2)

