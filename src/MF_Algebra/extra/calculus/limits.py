from ...expressions.combiners.combiners import Combiner
from ...expressions.functions.functions import Function, c0, arg
from ...expressions.variables import Variable


class Approaches(Combiner):
	def __init__(self, *children, **kwargs):
		super().__init__('\\to', 1, children=children, **kwargs)


class Superscript(Combiner):
	def __init__(self, *children, **kwargs):
		super().__init__('^', 0, children=children, **kwargs)


plus_symbol = Variable('+')
minus_symbol = Variable('-')


class Limit(Function):
	string_code = ['\\lim', '_', c0, arg]
	glyph_code = [3, c0, arg]
	def __init__(self, variable, value, direction='both', **kwargs):
		if direction == 'both':
			destination = value
		elif direction == 'left':
			destination = Superscript(value, minus_symbol)
		elif direction == 'right':
			destination = Superscript(value, plus_symbol)
		else:
			raise ValueError(f"Invalid direction: {direction}. Must be both, left, or right.")
		self.direction = direction
			
		super().__init__(
			children=[Approaches(variable, destination)],
			parentheses_mode='weak', 
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