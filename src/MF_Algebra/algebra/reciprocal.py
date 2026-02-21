from ..expressions import Div, a
from ..actions import Action, swap_children_, div_
from .algebra_core import AlgebraicAction



class reciprocal_(Action):
	swap = swap_children_()
	div = div_(1, side='left')
	# div = AlgebraicAction(a, 1/a, [[], '0/', {'delay':0.2}])
	def get_output_expression(self, input_expression):
		if isinstance(input_expression, Div):
			return self.swap.get_output_expression(input_expression)
		else:
			return self.div.get_output_expression(input_expression)
	
	def get_addressmap(self, input_expression, **kwargs):
		if isinstance(input_expression, Div):
			return self.swap.get_addressmap(input_expression, **kwargs)
		else:
			return self.div.get_addressmap(input_expression, **kwargs)

