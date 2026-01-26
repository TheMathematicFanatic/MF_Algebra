from ..expression_core import *
from .combiners import *


class Sequence(Combiner):
	symbol = ','
	symbol_glyph_length = 1
	def __init__(self, *children, generator=None, **kwargs):
		self.generator = generator
		super().__init__(*children, **kwargs)


class Coordinate(Sequence):
	parentheses = True

	def compute(self):
		return tuple(map(lambda N: N.compute(), self.children))
	
	def auto_parentheses(self):
		self.give_parentheses()
		for child in self.children:
			child.auto_parentheses()
		return self
