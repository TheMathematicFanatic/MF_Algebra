from .set_core import Set
from ..expressions import Expression, Sequence


class Interval(Set, Sequence):
	def __init__(self, a, b, **kwargs):
		super().__init__(a, b, **kwargs)
		assert a < b, "Interval lower bound must be less than upper bound"
		self.a = a
		self.b = b
		
	def in_rule(self, x):
		if isinstance(x, Expression):
			try: x = x.compute()
			except: return False
		if x < self.a: return False
		elif x == self.a: return self.paren_symbols[0] == '['
		elif self.a < x < self.b: return True
		elif x == self.b: return self.paren_symbols[1] == ']'
		elif self.b < x: return False



class OO_Interval(Interval):
	parentheses = True
	paren_symbols = ('(',')')

class CC_Interval(Interval):
	parentheses = True
	paren_symbols = ('[',']')

class OC_Interval(Interval):
	parentheses = True
	paren_symbols = ('(',']')

class CO_Interval(Interval):
	parentheses = True
	paren_symbols = ('[',')')

