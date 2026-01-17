from ..expression_core import *
from .functions import Function, child, arg
from ..numbers.integer import ten
from ..numbers.real import e
import math


class Log(Function):
	string_code = ['\\log_', child, arg]
	glyph_code = [3, child, arg]
	def __init__(self, base, **kwargs):
		kwargs.setdefault('parentheses_mode', 'strong')
		super().__init__(
			symbol = '\\log',
			children = [base],
			**kwargs
        )

	def python_rule(self, x):
		base = self.base.compute()
		return math.log(x, base)

	@property
	def base(self):
		return self.children[0]



class NaturalLog(Log):
	string_code = ['\\ln', arg]
	glyph_code = [2, arg]
	standard_form = Log(e)
ln = NaturalLog(e)



class CommonLog(Log):
	string_code = ['\\log', arg]
	glyph_code = [3, arg]
	standard_form = Log(ten)
log = CommonLog(10)
