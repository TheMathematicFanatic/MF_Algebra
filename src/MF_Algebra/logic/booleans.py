from ..expressions.expression_core import Expression, ExpressionContainer
from ..expressions.numbers import Number
from ..expressions.variables import Variable



class BooleanExpression(Expression):
	def __invert__(self):
		from .operations import Not
		return Not(self)

	def __neg__(self):
		from .operations import Not
		return Not(self)

	def __and__(self, other):
		from .operations import And
		return And(self, other)

	def __mul__(self, other):
		from .operations import And
		return And(self, other)

	def __or__(self, other):
		from .operations import Or
		return Or(self, other)

	def __xor__(self, other):
		from .operations import Xor
		return Xor(self, other)

	def __add__(self, other):
		from .operations import Xor
		return Xor(self, other)

	def __pow__(self, other):
		from .operations import Implies
		return Implies(self, other)

	def __floordiv__(self, other):
		from .operations import Iff
		return Iff(self, other)





class Boolean(BooleanExpression, Number):
	value_type = bool
	true_string = "\\textbf{T}"
	false_string = "\\textbf{F}"

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return 1

	@Expression.parenthesize_latex
	def __str__(self):
		return self.true_string if self.value else self.false_string

	def compute(self):
		return self.value



class BooleanVariable(BooleanExpression, Variable):
	pass


class BooleanVariables(ExpressionContainer):
	expression_type = BooleanVariable



A = BooleanVariable('A', 1)
B = BooleanVariable('B', 1)
C = BooleanVariable('C', 1)
D = BooleanVariable('D', 1)

T = Boolean(True)
F = Boolean(False)
