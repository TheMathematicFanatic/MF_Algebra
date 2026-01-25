from ..expressions.functions.functions import *
from .unit_circle import unit_circle_dict
import numpy as np



class TrigFunction(Function):
	def __init__(self,
		symbol = None,
		python_rule = None,
		**kwargs
	):
		super().__init__(
			symbol = symbol,
			python_rule = python_rule,
			parentheses_mode = 'weak',
			**kwargs
		)

	# def __pow__(self, other):
	# 	other = Smarten(other)
	# 	if other.compute() == -1:
	# 		return self.inverse()
	# 	else:
	# 		from .powers import TrigPower
	# 		return TrigPower(self, other)

	def inverse(self):
		pass
		from .inverses import Inverse



	


class Sine(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\sin',
			symbol_glyph_length = 3,
			python_rule = np.sin,
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][0]
		else:
			return super().evaluate(arg)


class Cosine(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\cos',
			symbol_glyph_length = 3,
			python_rule = np.cos,
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][1]
		else:
			return super().evaluate(arg)


class Tangent(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\tan',
			symbol_glyph_length = 3,
			python_rule = np.tan,
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][2]
		else:
			return super().evaluate(arg)


class Cosecant(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\csc',
			symbol_glyph_length = 3,
			python_rule = lambda x: 1/np.sin(x),
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][0].reciprocal()
		else:
			return super().evaluate(arg)


class Secant(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\sec',
			symbol_glyph_length = 3,
			python_rule = lambda x: 1/np.cos(x),
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][1].reciprocal()
		else:
			return super().evaluate(arg)


class Cotangent(TrigFunction):
	def __init__(self, **kwargs):
		super().__init__(
			symbol = '\\cot',
			symbol_glyph_length = 3,
			python_rule = lambda x: 1/np.tan(x),
			**kwargs
		)

	def evaluate(self, arg):
		if arg in unit_circle_dict:
			return unit_circle_dict[arg][2].reciprocal()
		else:
			return super().evaluate(arg)


sin = Sine()
cos = Cosine()
tan = Tangent()
csc = Cosecant()
sec = Secant()
cot = Cotangent()

