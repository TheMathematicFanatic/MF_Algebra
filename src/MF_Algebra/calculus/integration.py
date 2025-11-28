from ..actions import IncompatibleExpression
from ..algebra import AlgebraicAction
from ..timelines import AutoTimeline
from ..expressions.variables import a,b,n,v,u,v,x
from ..expressions.functions import f, g
from .integrals import I, Iab, IntegralOperator, PlugInBounds
from .differentials import DifferentialOperator, d, du, dv, dx
from ..expressions.numbers.number import Number
from ..expressions.functions import ln
from numpy import pi as PI
TAU = PI*2


class IntegralRule(AlgebraicAction):
	var_condition_dict = {
		d: lambda exp: isinstance(exp, DifferentialOperator),
		I: lambda exp: isinstance(exp, IntegralOperator),
		n: lambda exp: isinstance(exp, Number)
	}


class Int_ConstantMultiple_(IntegralRule):
	template1 =	I(n*u)
	template2 =	n*I(u)

class Int_ConstantMultiple_dx_(Int_ConstantMultiple_):
	template1 =	I(n*u*dx)
	template2 =	n*I(u*dx)

class Int_SumRule_(IntegralRule):
	template1 =	I(a+v)
	template2 =	I(a) + I(v)
	addressmap = [['1+', '+']]

class Int_SumRule_dx_(IntegralRule):
	template1 =	I((u+v)*dx)
	template2 =	I(u*dx) + I(v*dx)
	addressmap = [['10+', '+']]

class Int_DifferenceRule_(IntegralRule):
	template1 =	I(a-v)
	template2 =	I(a) - I(v)
	addressmap = [['1-', '-']]

class Int_DifferenceSumRule_dx_(IntegralRule):
	template1 =	I((u-v)*dx)
	template2 =	I(u*dx) - I(v*dx)
	addressmap = [['10-', '-']]


class IntegrationByParts_(IntegralRule):
	template1 =	I(u*dv)
	template2 =	u*v - I(v*du)
IBP_Indefinite_ = IntegrationByParts_

class IBP_definite_(IntegralRule):
	template1 = Iab(a,b)(u*dv)
	template2 = PlugInBounds(a,b)(u*v) - Iab(a,b)(v*du)



# class ChainRule(IntegralRule):
	# template1 = d(f(g(a)))
	# template2 = d(f)(g(a))*d(g(a)))
# Idk I think this could be just always built in to all other rules


from ..algebra.simplify import *
Simplify_Rules = [rule() for rule in SimplificationRule.__subclasses__()]
Derivative_Rules = [rule() for rule in IntegralRule.__subclasses__()]

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


