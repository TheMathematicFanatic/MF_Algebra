from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import two


class Rad(Function):
	def __init__(self, index, allow_nickname = True, **kwargs):
		self.allow_nickname = allow_nickname
		super().__init__(
			symbol = '\\sqrt',
			children = [index],
			parentheses_mode = 'never',
			**kwargs
        )

		self.init_caches()

	def init_caches(self):
		super().init_caches()
		if self.allow_nickname and self.index.is_identical_to(two):
			self.nicknamed = True
		else:
			self.nicknamed = False

	def python_rule(self, x):
		index = self.index.compute()
		return x**(1/index)

	@property
	def index(self):
		return self.children[0]

	@property
	def string_code(self):
		return [
			lambda self: self.symbol,
			'' if self.nicknamed else '[',
			'' if self.nicknamed else child,
			'' if self.nicknamed else ']',
			arg
		]

	@property
	def glyph_code(self):
		return [
			0 if self.nicknamed else child,
			lambda self: self.radical_glyph_count(),
			arg
		]

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


sqrt = Rad(2)

cbrt = Rad(3)
