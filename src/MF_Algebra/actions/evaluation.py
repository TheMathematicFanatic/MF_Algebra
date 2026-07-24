from ..expressions.expression_core import Expression
from .action_core import Action, IncompatibleExpression
from ..utils.color import average_color
from typing import Type, Literal


class evaluate_(Action):
	def __init__(
		self,
		allowed_type: Type[Expression] = None,
		color_mode: Literal[None, 'combine'] = None,
		**kwargs
	):
		self.color_mode = color_mode
		self.allowed_type = allowed_type
		super().__init__(**kwargs)

	def get_output_expression(self, input_expression=None):
		try:
			output = input_expression.evaluate()
			if self.allowed_type:
				assert isinstance(output, self.allowed_type)
		except:
			raise IncompatibleExpression
		if self.color_mode == 'combine':
			colors = [child.color for child in input_expression.children if child.color is not None]
			if colors:
				new_color = average_color(*colors)
				output.color = new_color
		return output

	def get_addressmap(self, input_expression=None):
		return [
			['', ''] # Extension by preaddress is done by decorator!
		]
	
