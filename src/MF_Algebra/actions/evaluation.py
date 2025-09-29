from .action_core import Action, IncompatibleExpression
from ..expressions.combiners.operations import Operation


class evaluate_(Action):
	def __init__(self, mode='random leaf', **kwargs):
		self.mode = mode # Idk if we will use this, seems like more of a Timeline decision
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		if isinstance(input_expression, Operation):
			return input_expression.evaluate()
		raise IncompatibleExpression

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression=None):
		return [
			['', ''] # Extension by preaddress is done by decorator!
		]
	
