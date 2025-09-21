from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import ten
from ..numbers.real import e
import math


class Log(Function):
	def __init__(self, base, allow_nickname = True, **kwargs):
		super().__init__(
			children = [base],
			parentheses_mode = 'strong',
			**kwargs
        )

		if allow_nickname and self.base.is_identical_to(ten):
			self.nicknamed = True
		elif allow_nickname and self.base.is_identical_to(e):
			self.nicknamed = 'ln'
		else:
			self.nicknamed = False

		def python_rule(x):
			base = self.base.compute()
			return math.log(x, base)
		self.python_rule = python_rule

	@property
	def base(self):
		return self.children[0]

	@property
	def string_code(self):
		return [
			'\\ln' if self.nicknamed == 'ln' else '\\log',
			'' if self.nicknamed else '_{',
			'' if self.nicknamed else child(0),
			'' if self.nicknamed else '}',
			'{', arg, '}'
		]

	@property
	def glyph_code(self):
		return [
			2 if self.nicknamed == 'ln' else 3,
			0 if self.nicknamed else child(0),
			arg
		]


ln = Log(e)
