from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import Integer


class Rad(Function):
	def __init__(self, index, allow_nickname = True, **kwargs):
		super().__init__(
			symbol = '\\sqrt',
			children = [index],
			parentheses_mode = 'never',
			**kwargs
        )
		if self.index.is_identical_to(Integer(2)) and allow_nickname:
			self.nicknamed = True
		else:
			self.nicknamed = False
		self.python_rule = lambda x: x**(1/self.index.compute())

	@property
	def index(self):
		return self.children[0]

	@property
	def string_code(self):
		return [
			lambda self: self.symbol,
			'' if self.nicknamed else '[',
			'' if self.nicknamed else child(0),
			'' if self.nicknamed else ']',
			'{',
			arg,
			'}'
		]

	@property
	def glyph_code(self):
		return [
			0 if self.nicknamed else child(0),
			lambda self: self.radical_glyph_count(),
			arg
		]

	def radical_glyph_count(self):
		if algebra_config['fast_root_length']:
			return 2
		else:
			raise NotImplementedError


sqrt = Rad(2)

cbrt = Rad(3)
