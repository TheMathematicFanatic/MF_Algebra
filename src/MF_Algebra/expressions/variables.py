from .expression_core import *


class Variable(Expression):
	def __init__(self, symbol, symbol_glyph_length=None, **kwargs):
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		super().__init__(**kwargs)

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if algebra_config['fast_glyph_count'] and not self.symbol_glyph_length:
			raise ValueError(f'Fast glyph count mode is on but {self} has no set glyph_length')
		return self.symbol_glyph_length

	@Expression.parenthesize_latex
	def __str__(self):
		return self.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")

	def hash_key(self):
		return (self.__class__, tuple(self.children), self.symbol)



a = Variable('a', 1)
b = Variable('b', 1)
c = Variable('c', 1)
# d = Variable('d', 1) # Differential
# e = Variable('e', 1) # Real
# f = Variable('f', 1) # Function
# g = Variable('g', 1) # Function
# h = Variable('h', 1) # Function
# i = Variable('i', 1) # Complex
j = Variable('j', 1)
k = Variable('k', 1)
l = Variable('l', 1)
m = Variable('m', 1)
n = Variable('n', 1)
o = Variable('o', 1)
p = Variable('p', 1)
q = Variable('q', 1)
r = Variable('r', 1)
s = Variable('s', 1)
t = Variable('t', 1)
u = Variable('u', 1)
v = Variable('v', 1)
w = Variable('w', 1)
x = Variable('x', 1)
y = Variable('y', 1)
z = Variable('z', 1)

alpha = Variable('\\alpha', 1)
beta = Variable('\\beta', 1)
gamma = Variable('\\gamma', 1)
theta = Variable('\\theta', 1)
phi = Variable('\\phi', 1)

dots = Variable('\\ldots', 3)
cdots = Variable('\\cdots', 3)


class Variables:
	# Nothing but a container so that you can make multiple variables at a time
	# A,B,C = Variables('ABC')
	# mu,chi,psi = Variables('\\mu', '\\chi', '\\psi')
	# You can set the glyph lengths in a list but it's really not a big deal if you don't.
	def __init__(self, *strings, symbol_glyph_length_list=None):
		if len(strings) == 1:
			self.strings = list(strings[0])
		else:
			self.strings = list(strings)
		self.symbol_glyph_length_list = symbol_glyph_length_list

	def __iter__(self):
		if self.symbol_glyph_length_list:
			assert len(self.strings) == len(self.symbol_glyph_length_list)
			return (Variable(s, l) for s, l in zip(self.strings, self.symbol_glyph_length_list))
		else:
			return (Variable(s) for s in self.strings)

