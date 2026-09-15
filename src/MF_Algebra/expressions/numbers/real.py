from ..expression_core import *
from .number import Number
import numpy as np


class Real(Number):
	value_type = float
	internal_precision = 10**-8
	def __init__(self, value, symbol=None, symbol_glyph_length=None, decimal_places=None, **kwargs):
		self._decimal_places = decimal_places
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		rounded = round(value, self.decimal_places)
		if np.abs(value - rounded) < self.internal_precision:
			value = rounded
		super().__init__(value, **kwargs)
	
	@property
	def decimal_places(self):
		return self._decimal_places if self._decimal_places is not None else algebra_config['decimal_places']
	
	@decimal_places.setter
	def decimal_places(self, num_places):
		if not isinstance(num_places, int) or num_places < 0:
			raise ValueError('decimal_places must be a non-negative integer')
		self._decimal_places = num_places

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if self.symbol:
			if self.symbol_glyph_length:
				return self.symbol_glyph_length
		else: # This needs work... parentheses are an issue.
			string = self.__str__.__wrapped__(self) # Ok this might do it but still seems a little stupid
			count = len(string)
			if string.endswith('\\ldots'): # Like fr? But it works lol
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
			return f'{self.value:.{self.decimal_places}f}' + '\\ldots'

	def is_negative(self):
		return self.value < 0
	
	def compute(self):
		if self.value.is_integer():
			return int(self.value)
		else:
			return self.value


e = Real(np.e, 'e', 1)
pi = Real(np.pi, '\\pi', 1)
tau = Real(np.pi*2, '\\tau', 1)
