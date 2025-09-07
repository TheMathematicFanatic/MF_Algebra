from .expression_core import *


class Variable(Expression):
	def __init__(self, symbol, symbol_glyph_length=None, **kwargs):
		super().__init__(**kwargs)
		self.symbol = symbol
		self._number_of_glyphs = symbol_glyph_length

	@Expression.parenthesize
	def __str__(self):
		return self.symbol

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")
