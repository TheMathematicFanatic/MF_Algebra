from .action_core import Action
from ..expressions.expression_core import Expression


class change_color_(Action):
	def __init__(self, color, **kwargs):
		self.color = color
		super().__init__(**kwargs)

	def get_output_expression(self, input_expression:Expression):
		input_expression.color = self.color
		input_expression.set_color_by_children()
		return input_expression


class give_parentheses_(Action):
	paren_bool = True
	paren_symbols = ('(',')')
	def __init__(self, paren_bool=None, paren_symbols=None, **kwargs):
		self.paren_bool = paren_bool or self.paren_bool
		self.paren_symbols = paren_symbols or self.paren_symbols
		super().__init__(**kwargs)

	def get_output_expression(self, input_expression:Expression):
		input_expression.give_parentheses(self.paren_bool, self.paren_symbols)
		return input_expression
	
	def get_addressmap(self, input_expression:Expression):
		if self.paren_bool and not input_expression.parentheses:
			return [[[], '()'], ['_', '_']]
		elif not self.paren_bool and input_expression.parentheses:
			return [['()', []], ['_', '_']]
		else:
			return [['', '']]


class remove_parentheses_(give_parentheses_):
	paren_bool = False
