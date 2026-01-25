from ..expression_core import *
from .number import Number
from ..combiners.operations import Div
from fractions import Fraction



class Rational(Number, Div):
	value_type = Fraction
	def __init__(self, a, b, **kwargs):
		self.value = Fraction(a, b)
		Div.__init__(self, Smarten(a), Smarten(b))

	def simplify(self):
		pass #idk will make 

	@property
	def numerator(self):
		return self.children[0]

	@property
	def denominator(self):
		return self.children[1]