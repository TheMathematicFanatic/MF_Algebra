from ..actions import IncompatibleExpression
from ..algebra import AlgebraicAction
from ..timelines import AutoTimeline
from ..expressions.variables import a, b, c
from ..expressions.functions import f, g
from .differentials import d, DifferentialOperator
from ..expressions.numbers.number import Number
from ..expressions.functions import ln
from numpy import pi as PI
TAU = PI*2



class DifferentialAction(AlgebraicAction):
	def __init__(self, *args, var_condition_dict={}, **kwargs):
		var_condition_dict.update({d: lambda exp: isinstance(exp, DifferentialOperator)})
		super().__init__(*args, var_condition_dict=var_condition_dict, **kwargs)


Derivative_Rules = [
	ConstantRule := DifferentialAction(
		d(c), 
		0,
		['', ''],
		var_condition_dict={c: lambda exp: isinstance(exp, Number)},
	),
	ConstantMultipleRule := DifferentialAction(
		d(c*a),
		c*d(a),
		var_condition_dict={c: lambda exp: isinstance(exp, Number)},
	),
	SumRule := DifferentialAction(
		d(a+b),
		d(a) + d(b),
		['+', '+']
	),
	DifferenceRule := DifferentialAction(
		d(a-b),
		d(a) - d(b),
		['-', '-']
	),
	ProductRule := DifferentialAction(
		d(a*b),
		b*d(a) + a*d(b),
		['*', '+'], [[], '0*'], [[], '1*'],
	),
	QuotientRule := DifferentialAction(
		d(a/b),
		(b*d(a) - a*d(b))/b**2,
	),
	PowerRule := DifferentialAction(
		d(a**b),
		b*a**(b-1)*d(a),
		['11', '0110'],
		[[], '011-1'],
		var_kwarg_dict={b:{'path_arc':TAU/3}},
		var_condition_dict={b: lambda exp: isinstance(exp, Number)},
	),
	ExponentialRule := DifferentialAction(
		d(a**b),
		ln(a)*a**b*d(b),
		[[], '00f0()'],
		var_condition_dict={a: lambda exp: isinstance(exp, Number)}
	)
	# ChainRule := AlgebraicAction(d(f(g(a))), d(f)(g(a))*d(g(a)))
]

from ..algebra.simplify import *
Simplify_Rules = [rule() for rule in SimplificationRule.__subclasses__()]

class Differentiate(AutoTimeline):
	def decide_next_action(self, index):
		last_exp = self.get_expression(-1)
		for ad in last_exp.get_all_addresses():
			for ruleset in [Derivative_Rules, Simplify_Rules]:
				for rule in ruleset:
					try:
						action = rule.copy().pread(ad)
						action.get_output_expression(last_exp)
						return action
					except IncompatibleExpression:
						pass
		for ad in last_exp.get_all_twig_addresses():
			try:
				from ..actions.evaluation import evaluate_
				action = evaluate_().copy().pread(ad)
				action.get_output_expression(last_exp)
				return action
			except IncompatibleExpression:
				pass
		return None


