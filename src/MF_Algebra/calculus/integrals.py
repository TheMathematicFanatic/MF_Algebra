from ..expressions.functions.functions import Function, c0, c1, arg
from ..expressions.combiners.relations import Equation


class IntegralOperator(Function):
	pass


class DefiniteIntegral(IntegralOperator):
	string_code = [lambda self: self.symbol, '\\limits', '_', c0, '^', c1, arg]
	glyph_code = [c1, 1, c0, arg]
	def __init__(self, start, end, variable=None, show_variable=False, **kwargs):
		self.variable = variable
		if show_variable:
			assert variable is not None, "variable must be provided if show_variable is True"
			lower_bound = Equation(variable, start)
			upper_bound = Equation(variable, end)
		else:
			lower_bound = start
			upper_bound = end
		super().__init__(
			symbol = '\\int',
			symbol_glyph_length = 1,
			children = [lower_bound, upper_bound],
			parentheses_mode = 'weak',
			**kwargs
		)

	@property
	def lower_bound(self):
		return self.children[0]

	@property
	def upper_bound(self):
		return self.children[1]



class IndefiniteIntegral(IntegralOperator):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\int',
			symbol_glyph_length = 1,
			parentheses_mode = 'weak',
			**kwargs
		)

Integral = DefiniteIntegral
I = IndefiniteIntegral()



class PlugInBounds(Function):
	# string_code = ['\\quad', '\\left.', arg, '\\right\\rvert', '_', c0, '^', c1]
	string_code = ['\\quad', arg, '\\Bigg\\rvert', '_', c0, '^', c1]
	glyph_code = [arg, 3, c1, c0]
	def __init__(self, lower_bound, upper_bound, variable, show_variable=False):
		self.variable = variable
		self.show_variable = show_variable
		if show_variable:
			lower_bound = Equation(variable, lower_bound)
			upper_bound = Equation(variable, upper_bound)
		else:
			lower_bound = lower_bound
			upper_bound = upper_bound
		super().__init__(
			children = [lower_bound, upper_bound],
			parentheses_mode = 'weak'
		)
	
	@property
	def lower_bound(self):
		if self.show_variable:
			return self.get_subex('01')
		else:
			return self.get_subex('0')

	@property
	def upper_bound(self):
		if self.show_variable:
			return self.get_subex('11')
		else:
			return self.get_subex('1')

	def expand_on_args(self, arg):
		return arg @ {self.variable:self.upper_bound} - arg @ {self.variable:self.lower_bound}