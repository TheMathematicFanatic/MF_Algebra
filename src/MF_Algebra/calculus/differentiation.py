from ..actions import IncompatibleExpression
from ..algebra import AlgebraicAction
from ..timelines import AutoTimeline
from ..expressions import Variables, f, g, e, ln, Number
from ..trigonometry import *
from .differentials import *
from numpy import pi as PI
TAU = PI*2

x,y,n = Variables('xyn')

class DerivativeRule(AlgebraicAction):
	var_condition_dict = {
		d: lambda exp: isinstance(exp, DifferentialOperator),
		n: lambda exp: isinstance(exp, Number)
	}


class ConstantRule_(DerivativeRule):
	template1 =	d(n)
	template2 =	0

class ConstantMultipleRule_(DerivativeRule):
	template1 =	d(n*x)
	template2 =	n*d(x)

class SumRule_(DerivativeRule):
	template1 =	d(x+y)
	template2 =	d(x) + d(y)
	addressmap = [['+', '+']]

class DifferenceRule_(DerivativeRule):
	template1 =	d(x-y)
	template2 =	d(x) - d(y)
	addressmap = [['-', '-']]

class ProductRule_(DerivativeRule):
	template1 =	d(x*y)
	template2 =	y*d(x) + x*d(y)
	addressmap = [['*', '+'], [[], '0*'], [[], '1*']]

class QuotientRule_(DerivativeRule):
	template1 =	d(x/y)
	template2 =	(y*d(x) - x*d(y)) / y**2

class PowerRule_(DerivativeRule):
	template1 =	d(x**n)
	template2 =	n * x**(n-1) * d(x)
	addressmap = [['11', '0110'], [[], '011-1']]
	var_kwarg_dict = {n:{'path_arc':TAU/3}}

class ExponentialRule_(DerivativeRule):
	template1 =	d(n**x)
	template2 =	ln(n) * n**x * d(x)
	addressmap = [[[], '000']]

# class ChainRule(DerivativeRule):
	# template1 = d(f(g(a)))
	# template2 = d(f)(g(a))*d(g(a)))
# Idk I think this could be just always built in to all other rules

function_derivatives = [
	( e**x, e**x ),
	( ln(x), 1/x ),
	( sin(x), cos(x) ),
	( cos(x), -sin(x) ),
	( tan(x), (sec**2)(x) ),
	( arcsin(x), 1/sqrt(1-x**2) ),
	( arccos(x), -1/sqrt(1-x**2) ),
	( arctan(x), 1/(1+x**2) ),
]

for func1, func2 in function_derivatives:
	f1_x_ad = func1.get_addresses_of_subex(x)[0]
	f2_x_ad = func2.get_addresses_of_subex(x)[0]
	class deriv_func_rule(DerivativeRule):
		template1 = d(func1)
		template2 = func2*dx
		addressmap = [
			[f1_x_ad+'1', f2_x_ad+'0'],
			['!'+f1_x_ad+'1', '!'+f2_x_ad+'0']
		]



from ..algebra.simplify import *
Simplify_Rules = [rule() for rule in SimplificationRule.__subclasses__()]
Derivative_Rules = [rule() for rule in DerivativeRule.__subclasses__()]

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




