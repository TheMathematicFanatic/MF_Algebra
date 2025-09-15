from .expression_core import *


class Variable(Expression):
	def __init__(self, symbol, symbol_glyph_length=None, **kwargs):
		super().__init__(**kwargs)
		self.symbol = symbol
		self._number_of_glyphs = symbol_glyph_length

	@Expression.parenthesize
	def __str__(self):
		return self.symbol

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")


a = Variable('a')
b = Variable('b')
c = Variable('c')

k = Variable('k')
m = Variable('m')
n = Variable('n')

p = Variable('p')
q = Variable('q')
r = Variable('r')

t = Variable('t')
u = Variable('u')
v = Variable('v')

x = Variable('x')
y = Variable('y')
z = Variable('z')

alpha = Variable('\\alpha')
beta = Variable('\\beta')
gamma = Variable('\\gamma')
theta = Variable('\\theta')
phi = Variable('\\phi')

