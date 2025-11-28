from ..actions import IncompatibleExpression
from ..algebra import AlgebraicAction
from ..timelines import AutoTimeline
from ..expressions import Variables, f, g, e, ln, Number
from .integrals import *
from .differentials import DifferentialOperator, d, du, dv, dx
from numpy import pi as PI
TAU = PI*2

a,b,c,n,u,v,x,C = Variables('abcnuvxC')

class IntegralRule(AlgebraicAction):
	var_condition_dict = {
		d: lambda exp: isinstance(exp, DifferentialOperator),
		I: lambda exp: isinstance(exp, IntegralOperator),
		n: lambda exp: isinstance(exp, Number)
	}

class FundThmCalc_1_(IntegralRule):
	template1 = d(DefiniteIntegral(n,x)(u*dx))
	template2 = u

class FundThmCalc_2_(IntegralRule):
	template1 = DefiniteIntegral(a,b)(du)
	template2 = PlugInBounds(a,b,x)(u)

class Int_dx_(IntegralRule):
	template1 = I(d(u))
	template2 = u

class d_Int_x_(IntegralRule):
	template1 = d(I(u))
	template2 = u

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

class Int_PowerRule_dx_(IntegralRule):
	template1 = I(x**n*dx)
	template2 = 1/(n+1)*x**(n+1)
	var_condition_dict = {
		n: lambda exp: isinstance(exp, Number) and not exp == -1
	}

class Int_DifferenceSumRule_dx_(IntegralRule):
	template1 =	I((u-v)*dx)
	template2 =	I(u*dx) - I(v*dx)
	addressmap = [['10-', '-']]


class IntegrationByParts_(IntegralRule):
	template1 =	I(u*dv)
	template2 =	u*v - I(v*du)
IBP_indefinite_ = IntegrationByParts_

# class IBP_definite_(IntegralRule):
# 	template1 = DefiniteIntegral(a,b)(u*dv)
# 	template2 = PlugInBounds(a,b)(u*v) - DefiniteIntegral(a,b)(v*du)
# not sure how to do pluginbounds' variable. Do we even need this though?


from ..algebra.simplify import *
Simplify_Rules = [rule() for rule in SimplificationRule.__subclasses__()]
Integral_Rules = [rule() for rule in IntegralRule.__subclasses__()]

class Integrate(AutoTimeline):
	def decide_next_action(self, index):
		last_exp = self.get_expression(-1)
		for ad in last_exp.get_all_addresses():
			for ruleset in [Integral_Rules, Simplify_Rules]:
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


