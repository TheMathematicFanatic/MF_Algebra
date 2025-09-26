from ...actions.algebra.algebra_core import AlgebraicAction
from ...expressions.variables import a, b
from ...expressions.functions import f, g
from .differentials import d

Derivative_Rules = [
	SumRule := AlgebraicAction(d(a+b), d(a) + d(b)),
	DifferenceRule := AlgebraicAction(d(a-b), d(a) - d(b)),
	ProductRule := AlgebraicAction(d(a*b), b*d(a) + a*d(b)),
	QuotientRule := AlgebraicAction(d(a/b), (b*d(a) - a*d(b))/b**2),
	PowerRule := AlgebraicAction(d(a**b), b*a**(b-1)*d(a)),
	# ChainRule := AlgebraicAction(d(f(g(a))), d(f)(g(a))*d(g(a)))
]





