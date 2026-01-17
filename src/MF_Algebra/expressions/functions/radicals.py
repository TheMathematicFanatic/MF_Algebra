from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import two


class Rad(Function):
	string_code = ['\\sqrt', '[', child, ']', arg]
	glyph_code = [child, lambda self: self.radical_glyph_count(), arg]
	def __init__(self, index, **kwargs):
		super().__init__(
			symbol = '\\sqrt',
			children = [index],
			parentheses_mode = 'never',
			**kwargs
        )

	def python_rule(self, x):
		index = self.index.compute()
		return x**(1/index)

	@property
	def index(self):
		return self.children[0]

	def radical_glyph_count(self):
		if algebra_config['fast_root_length']:
			return 2
		else:
			raise NotImplementedError
	
	# def expand_on_args(self, arg, mode='rational_exponent'):
	# 	if mode == 'rational_exponent':
	# 		return arg ** (1 / self.index)
	# 	else:
	# 		raise NotImplementedError

class SquareRoot(Rad):
	string_code = ['\\sqrt', arg]
	glyph_code = [2, arg]
	def __init__(self, **kwargs):
		super().__init__(2, **kwargs)
sqrt = SquareRoot()

cbrt = Rad(3)
