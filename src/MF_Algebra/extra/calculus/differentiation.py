from ...actions import AlgebraicAction, IncompatibleExpression
from ...timelines import AutoTimeline
from ...expressions.variables import a, b, c
from ...expressions.functions import f, g
from .differentials import d, DifferentialOperator
from ...expressions.numbers.number import Number


class DifferentialAction(AlgebraicAction):
	def __init__(self, template1, template2, var_condition_dict={}, **kwargs):
		var_condition_dict.update({d: lambda exp: isinstance(exp, DifferentialOperator)})
		super().__init__(template1, template2, var_condition_dict, **kwargs)


Derivative_Rules = [
	ConstantRule := DifferentialAction(d(c), 0, {c: lambda exp: isinstance(exp, Number)}),
	SumRule := DifferentialAction(d(a+b), d(a) + d(b)),
	DifferenceRule := DifferentialAction(d(a-b), d(a) - d(b)),
	ProductRule := DifferentialAction(d(a*b), b*d(a) + a*d(b)),
	QuotientRule := DifferentialAction(d(a/b), (b*d(a) - a*d(b))/b**2),
	PowerRule := DifferentialAction(d(a**b), b*a**(b-1)*d(a), {b: lambda exp: isinstance(exp, Number)}),
	# ChainRule := AlgebraicAction(d(f(g(a))), d(f)(g(a))*d(g(a)))
]


class Differentiate(AutoTimeline):
	def decide_next_action(self, index):
		last_exp = self.get_expression(-1)
		d_addresses = last_exp.get_addresses_of_subex(d)
		for d_ad in d_addresses:
			for DR in Derivative_Rules:
				try:
					action = DR.pread(d_ad[:-1])
					action.get_output_expression(last_exp)
					return action
				except IncompatibleExpression:
					pass
		



