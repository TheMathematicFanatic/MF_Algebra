from .expression_core import *
from .operations import Div
import numpy as np


class Number(Expression):
	def __init__(self, **kwargs):
		self.children = []
		self.value = None
		super().__init__(**kwargs)

	def compute(self):
		return float(self)
	
	def number_of_glyphs(self):
		return len(str(self.value))


class Integer(Number):
	def __init__(self, n, **kwargs):
		assert isinstance(n, int)
		super().__init__(**kwargs)
		self.value = n

	@parenthesize
	def __str__(self):
		return str(self.value)

	def __float__(self):
		return float(self.value)
	
	def compute(self):
		return self.value

	def is_identical_to(self, other):
		return type(self) == type(other) and self.value == other.value

	def is_negative(self):
		return self.value < 0

	@staticmethod
	def GCF(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.value, smartnums))
		return Smarten(int(np.gcd.reduce(nums)))

	@staticmethod
	def LCM(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.value, smartnums))
		return Smarten(int(np.lcm.reduce(nums)))

	def prime_factorization(self):
		...


class Real(Number):
	def __init__(self, x, symbol=None, symbol_glyph_length=1, **kwargs):
		super().__init__(**kwargs)
		self.value = x
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length

	@parenthesize
	def __str__(self, decimal_places=4, use_decimal=False):
		if self.symbol and not use_decimal:
			return self.symbol
		rounded = round(self.value, decimal_places)
		if rounded == self.value:
			return str(rounded)
		else:
			return f"{self.value:.{decimal_places}f}" + r"\ldots"
	
	def number_of_glyphs(self):
		if self.symbol:
			return self.symbol_glyph_length
		else:
			string = str(self)
			if string.endswith(r"\ldots"):
				return len(string) - 3
			else:
				return len(string)

	def __float__(self):
		return float(self.value)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.value == other.value

	def is_negative(self):
		return self.value < 0
	
	def compute(self):
		if self.value.is_integer():
			return int(self.value)
		else:
			return self.value


class Rational(Div):
	# Better to subclass Div than Number because 5/3 is no more a number than 5^3 or 5+3
	# Multiclassing is an option but seems to be more trouble than it's worth
	def __init__(self, a, b, **kwargs):
		if not isinstance(a, (Integer, int)):
			raise TypeError (f"Unsupported numerator type {type(a)}: {a}")
		if not isinstance(b, (Integer, int)):
			raise TypeError (f"Unsupported denominator type {type(b)}: {b}")
		super().__init__(a, b, **kwargs)

	def simplify(self):
		pass #idk will make later
