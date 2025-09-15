from ..expression_core import *
from .number import *


class Integer(Number):
	def __init__(self, n, **kwargs):
		assert isinstance(n, int)
		super().__init__(**kwargs)
		self.value = n

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return len(str(self.value))

	@Expression.parenthesize_latex
	def __str__(self):
		return str(self.value)
	
	def compute(self):
		return self.value

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
		pass


zero = Integer(0)
one = Integer(1)
two = Integer(2)
three = Integer(3)
four = Integer(4)
five = Integer(5)
six = Integer(6)
seven = Integer(7)
eight = Integer(8)
nine = Integer(9)
ten = Integer(10)
