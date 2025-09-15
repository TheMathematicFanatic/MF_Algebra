from .expression_core import *


class Sequence(Combiner):
	def __init__(self, *children, generator=None, **kwargs):
		self.generator = generator
		super().__init__(",", 1, children=children, **kwargs)


class Coordinate(Sequence):
	def __init__(self, *children, **kwargs):
		super().__init__(*children, parentheses=True, **kwargs)
