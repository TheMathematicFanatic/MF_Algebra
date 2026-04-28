from .operations import BinaryOperation, Add, Sub
from ...actions.apply_operation import apply_binary_operation_
import numpy as np



class Eml(BinaryOperation):
	symbol = '\\epsilon'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x, y: np.exp(x) - np.log(y))

	def evaluate(self):
		from ..numbers import e
		from ..functions import ln
		x,y = self.children
		return e**x - ln(y)

	def auto_parentheses(self):
		for i, child in enumerate(self.children):
			if isinstance(child, (Add, Sub, Eml)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()
		return self

class equals_(apply_binary_operation_):
	OpClass = Eml


