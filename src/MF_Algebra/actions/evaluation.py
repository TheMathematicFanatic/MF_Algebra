from .action_core import Action, IncompatibleExpression
from ..expressions.combiners.operations import Operation
from ..expressions.numbers.number import Number


class evaluate_(Action):
	def __init__(self, mode='random leaf', allowed_type=Number, **kwargs):
		self.mode = mode # Idk if we will use this, seems like more of a Timeline decision
		self.allowed_type = Number
		super().__init__(**kwargs)

	def get_output_expression(self, input_expression=None):
		try:
			output = input_expression.evaluate()
			assert isinstance(output, self.allowed_type)
			return output
		except:
			raise IncompatibleExpression

	def get_addressmap(self, input_expression=None):
		return [
			['', ''] # Extension by preaddress is done by decorator!
		]
	
