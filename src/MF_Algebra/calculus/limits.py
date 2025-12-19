from ..expressions.combiners.combiners import Combiner, Superscript
from ..expressions.functions.functions import Function, c0, arg
from ..expressions.variables import Variable
from ..expressions.numbers.real import Real
import numpy as np


class Infinity(Real):
    def __init__(self, **kwargs):
        super().__init__(np.inf, '\\infty', **kwargs)
inf = Infinity()


class Approaches(Combiner):
	symbol = '\\to'
	symbol_glyph_length = 1


class Limit(Function):
	string_code = ['\\lim', '\\limits', '_', c0, arg]
	glyph_code = [3, c0, arg]
	def __init__(self, variable, value, direction='both', **kwargs):
		if direction == 'both':
			destination = value
		elif direction == 'left':
			destination = Superscript(value, Variable('-'))
		elif direction == 'right':
			destination = Superscript(value, Variable('+'))
		else:
			raise ValueError(f"Invalid direction: {direction}. Must be both, left, or right.")
		self.direction = direction
			
		super().__init__(
			children = [Approaches(variable, destination)],
			parentheses_mode = 'weak', 
			**kwargs
		)

	@property
	def variable(self):
		return self.get_subex('00')
	
	@property
	def destination(self):
		destination = self.get_subex('01')
		if isinstance(destination, Superscript):
			return destination.get_subex('0')
		else:
			return destination