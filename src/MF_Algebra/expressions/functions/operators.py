from .functions import Function, c0, c1, arg
from ..combiners.relations import Equation
from ..combiners.operations import *


class BigOperator(Function):
	string_code = [lambda self: self.symbol, '_{', c0, '}^{', c1, '}', arg]
	glyph_code = [c1, 1, c0, arg]
	def __init__(self, variable, start, end, **kwargs):
		super().__init__(
			children=[Equation(variable, start), end],
			parentheses_mode='weak', 
			**kwargs
		)

	@property
	def variable(self):
		return self.get_subex('00')

	@property
	def start(self):
		return self.get_subex('01').compute()

	@property
	def end(self):
		return self.get_subex('1').compute()

	def get_term(self, index):
		pass # Hmm wait a second.... the Function itself doesn't even have the argument to plug into.... ughhhh

	def expand(self, min=None, max=None, max_num_terms=7):
		if min is None:
			min = self.start
		if max is None:
			max = self.end
		assert min <= max
		if max - min > max_num_terms:
			terms = [self.get_term(i) for i in range(min, min+max_num_terms)]
			from ..variables import dots
			terms.append(dots)
		return self.opclass(*[self.get_term(i) for i in range(min, max+1)])


class Sum(BigOperator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.symbol = '\\sum'
		self.symbol_glyph_length = 1
		self.opclass = Add


class Product(BigOperator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.symbol = '\\prod'
		self.symbol_glyph_length = 1
		self.opclass = Mul






