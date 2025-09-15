from ..expression_core import *
from .number import *
from .integer import Integer


class Rational(Div):
	# Better to subclass Div than Number because 5/3 is no more a number than 5^3 or 5+3
	# Multiclassing is an option but seems to be more trouble than it's worth
	# Actually, I'm not so sure. Sometime I'd like to implement rational arithmetic and idk the best way
	def __init__(self, a, b, **kwargs):
		if not isinstance(a, (Integer, int)):
			raise TypeError (f"Unsupported numerator type {type(a)}: {a}")
		if not isinstance(b, (Integer, int)):
			raise TypeError (f"Unsupported denominator type {type(b)}: {b}")
		super().__init__(a, b, **kwargs)

	def simplify(self):
		pass #idk will make later