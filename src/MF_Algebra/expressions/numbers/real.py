from ..expression_core import *
from .number import *


class Real(Number):
	decimal_places = algebra_config['decimal_precision']
	def __init__(self, value, symbol=None, symbol_glyph_length=None, decimal_places=None, **kwargs):
		super().__init__(**kwargs)
		self.value = value
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		if decimal_places is not None:
			self.decimal_places = decimal_places

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if self.symbol:
			if self.symbol_glyph_length:
				return self.symbol_glyph_length
		else: # This needs work... parentheses are an issue.
			string = self.__str__.__wrapped__(self) # Ok this might do it but still seems a little stupid
			count = len(string)
			if string.endswith(r"\ldots"): # Like fr? But it works lol
				count -= 3
			return count

	@Expression.parenthesize_latex
	def __str__(self, use_decimal=False):
		if self.symbol and not use_decimal:
			return self.symbol
		rounded = round(self.value, self.decimal_places)
		if rounded == self.value:
			return str(rounded)
		else:
			return f"{self.value:.{self.decimal_places}f}" + r"\ldots"

	def is_negative(self):
		return self.value < 0
	
	def compute(self):
		if self.value.is_integer():
			return int(self.value)
		else:
			return self.value


e = Real(np.e, "e")
pi = Real(np.pi, "\\pi")
tau = Real(np.pi*2, "\\tau")
