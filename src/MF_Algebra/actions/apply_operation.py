from .action_core import Action
from ..expressions.combiners.operations import Add, Sub, Mul, Div, Pow
from ..expressions.combiners.relations import Equation
from ..expressions.functions.functions import ApplyFunction
from ..utils import Smarten
from MF_Tools.dual_compatibility import Write


class apply_operation_(Action):
	OpClass = None
	def __init__(self, other, side='right', introducer=Write, **kwargs):
		self.other = Smarten(other)
		self.side = side
		self.introducer = introducer
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression):
		if self.side == 'right':
			output_expression = self.OpClass(input_expression, self.other)
		elif self.side == 'left':
			output_expression = self.OpClass(self.other, input_expression)
		else:
			raise ValueError(f'Invalid side: {self.side}. Must be left or right.')
		return output_expression

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression):
		if self.side == 'right':
			return [
				['', '0'],
				[self.introducer, '+', {'delay':0.5}],
				[self.introducer, '1', {'delay':0.6}]
			]
		elif self.side == 'left':
			return [
				['', '1'],
				[self.introducer, '0', {'delay':0.5}],
				[self.introducer, '+', {'delay':0.6}]
			]
		else:
			raise ValueError(f'Invalid side: {self.side}. Must be left or right.')

	def __repr__(self):
		return type(self).__name__ + '(\'' + str(self.preaddress) + '\', ' + str(self.other) + ')'


class add_(apply_operation_):
	OpClass = Add

class sub_(apply_operation_):
	OpClass = Sub

class mul_(apply_operation_):
	OpClass = Mul

class div_(apply_operation_):
	OpClass = Div

class pow_(apply_operation_):
	OpClass = Pow

class equals_(apply_operation_):
	OpClass = Equation

class apply_func_(apply_operation_):
	OpClass = ApplyFunction
	def __init__(self, *args, **kwargs):
		super().__init__(*args, side='left', **kwargs)
