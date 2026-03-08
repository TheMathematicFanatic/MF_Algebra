from ..expressions.functions import Function, c0, arg
from ..sets import IsElement


class Quantifier(Function):
	string_code = [lambda self: self.symbol, c0, arg]
	glyph_code = [lambda self: self.symbol_glyph_length, c0, arg]
	def __init__(self, var, set=None):
		if set:
			child = IsElement(var, set)
		else:
			child = var
		super().__init__(
			children=[child],
			parentheses_mode='never'
		)


class ForAll(Quantifier):
	eval_op = staticmethod(lambda L: all(L))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.symbol = '\\forall'
		self.symbol_glyph_length = 1


class Exists(Quantifier):
	eval_op = staticmethod(lambda L: any(L))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.symbol = '\\exists'
		self.symbol_glyph_length = 1


class UniqueExists(Quantifier):
	eval_op = staticmethod(lambda L: sum(L) == 1)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.symbol = '\\exists{!}'
		self.symbol_glyph_length = 2
