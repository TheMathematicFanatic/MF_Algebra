from .functions import Function, child, arg


class AbsoluteValue(Function):
	string_code = ['\\left|', arg, '\\right|']
	glyph_code = [1, arg, 1]
	def __init__(self, **kwargs):
		super().__init__(
			python_rule = abs,
			parentheses_mode = 'never',
			**kwargs
		)
abs_value = AbsoluteValue()


class Factorial(Function):
	string_code = [arg, '!']
	glyph_code = [arg, 1]
	def __init__(self, **kwargs):
		from scipy.special import gamma
		super().__init__(
			python_rule = lambda z: gamma(z+1),
			parentheses_mode = 'strong',
			**kwargs
		)
fact = Factorial()


