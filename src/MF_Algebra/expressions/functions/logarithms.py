from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import ten
from ..numbers.real import e
import math


class Log(Function):
	def __init__(self, base, allow_nickname = True, **kwargs):
		kwargs.setdefault('parentheses_mode', 'strong')
		self.allow_nickname = allow_nickname
		super().__init__(
			children = [base],
			**kwargs
        )

		self.init_caches()

	def init_caches(self):
		super().init_caches()
		if self.allow_nickname and self.base.is_identical_to(ten):
			self.nicknamed = True
		elif self.allow_nickname and self.base.is_identical_to(e):
			self.nicknamed = 'ln'
		else:
			self.nicknamed = False

	def python_rule(self, x):
		base = self.base.compute()
		return math.log(x, base)

	@property
	def base(self):
		return self.children[0]

	@property
	def string_code(self):
		return [
			'\\ln' if self.nicknamed == 'ln' else '\\log',
			'' if self.nicknamed else '_',
			'' if self.nicknamed else child,
			arg
		]

	@property
	def glyph_code(self):
		return [
			2 if self.nicknamed == 'ln' else 3,
			0 if self.nicknamed else child,
			arg
		]


ln = Log(e)
