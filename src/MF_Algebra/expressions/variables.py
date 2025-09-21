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
		other = Smarten(other)
		return super().is_identical_to(other) and self.symbol == other.symbol

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

dots = Variable('\\ldots', 3)

x1 = x.subscript(1)
x2 = x.subscript(2)
x3 = x.subscript(3)
y1 = y.subscript(1)
y2 = y.subscript(2)
y3 = y.subscript(3)
z1 = z.subscript(1)
z2 = z.subscript(2)
z3 = z.subscript(3)

