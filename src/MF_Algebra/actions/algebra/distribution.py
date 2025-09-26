from ..action_core import Action
from ...expressions.combiners.operations import Add, Sub, Mul, Div, Pow


class distribute_(Action):
	# Not done yet, multilayer does not work... this is so necessary but rather nontrivial... hm...
	def __init__(self, mode='auto', multilayer=False, **kwargs):
		self.mode = mode #'auto', 'left', 'right'
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		if self.mode == 'auto':
			self.determine_direction(input_expression)
		if self.mode == 'left':
			new_children = [
				type(input_expression)(input_expression.children[0], child)
				for child in input_expression.children[-1].children
				]
			return type(input_expression.children[-1])(*new_children)
		elif self.mode == 'right':
			new_children = [
				type(input_expression)(child, input_expression.children[-1])
				for child in input_expression.children[0].children
				]
			return type(input_expression.children[0])(*new_children)

	def determine_direction(self, input_expression=None):
		if self.mode == 'auto':
			if isinstance(input_expression, Mul):
				left_distributable = isinstance(input_expression.children[-1], (Add, Sub))
				right_distributable = isinstance(input_expression.children[0], (Add, Sub))
				if left_distributable and right_distributable:
					raise ValueError('Cannot auto-distribute if both sides are distributable, please set mode manually.')
				elif left_distributable:
					self.mode = 'left'
				elif right_distributable:
					self.mode = 'right'
				else:
					raise ValueError('Cannot distribute, neither side is distributable.')
			elif isinstance(input_expression, Div):
				right_distributable = isinstance(input_expression.children[0], (Add, Sub))
				if right_distributable:
					self.mode = 'right'
				else:
					raise ValueError('Cannot distribute, right side is not distributable.')
			elif isinstance(input_expression, Pow):
				right_distributable = isinstance(input_expression.children[0], (Mul, Div))
				if right_distributable:
					self.mode = 'right'
				else:
					raise ValueError('Cannot distribute, right side is not distributable.')
			else:
				raise ValueError('Cannot auto-distribute, must be a multiplication or division.')

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression=None):
		return [
			['', ''] #standin idk what the fuck im doing here
		]
