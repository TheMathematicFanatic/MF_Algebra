from ...expressions.functions.functions import Function, c0, c1, arg
from ...expressions.combiners.relations import Equation



class DefiniteIntegral(Function):
	string_code = [lambda self: self.symbol, '_', c0, '^', c1, arg]
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



class IndefiniteIntegral(Function):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\int',
			symbol_glyph_length = 1,
			parentheses_mode = 'weak',
			**kwargs
		)