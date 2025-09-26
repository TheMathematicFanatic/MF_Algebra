from .functions import Function, child, arg, arg0, arg1


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


from ..variables import n, k
class BinomialCoefficient(Function):
	def __init__(self, mode='binom', **kwargs):
		self.mode = mode
		super().__init__(
			algebra_rule_variables = [n,k],
			algebra_rule = fact(n) / (fact(k) * fact(n-k)),
			parentheses_mode = 'never',
			**kwargs
		)

	@property
	def	string_code(self):
		if self.mode == 'binom':
			return ['\\binom', arg0, arg1]
		elif self.mode == 'nCk':
			return ['_', arg0, 'C', '_', arg1]
		elif self.mode == 'C(n,k)':
			return ['C', arg]
		else:
			raise ValueError(f"Invalid binomial coefficient mode: {self.mode}. Mode must be among ['binom', 'nCk', 'C(n,k)']")

	@property
	def glyph_code(self):
		if self.mode == 'binom':
			return [1, arg0, arg1, 1]
		elif self.mode == 'nCk':
			return [arg0, 1, arg1]
		elif self.mode == 'C(n,k)':
			return Function.glyph_code
		else:
			raise ValueError(f"Invalid binomial coefficient mode: {self.mode}. Mode must be among ['binom', 'nCk', 'C(n,k)']")


binom = BinomialCoefficient()
nCk = BinomialCoefficient(mode='nCk')



