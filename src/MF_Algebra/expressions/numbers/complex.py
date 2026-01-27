from ..expression_core import *
from .number import *


class Complex(Number):
	value_type = complex
	@Expression.parenthesize_latex
	def __str__(self):
		assert isinstance(self.value, complex)
		if self.value == 1j:
			return 'i'



i = Complex(1j)
