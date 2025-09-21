from ...actions.algebra import AlgebraicAction
from ...expressions.variables import a, b
from .differentials import d


# None of this works currently due to a problem in Function lol
SumRule = AlgebraicAction(d(a+b), d(a) + d(b))
DifferenceRule = AlgebraicAction(d(a-b), d(a) - d(b))
ProductRule = AlgebraicAction(d(a*b), d(a)*b + a*d(b))
QuotientRule = AlgebraicAction(d(a/b), (d(a)*b - a*d(b))/b**2)
PowerRule = AlgebraicAction(d(a**b), b*d(a**(b-1))*d(a))





