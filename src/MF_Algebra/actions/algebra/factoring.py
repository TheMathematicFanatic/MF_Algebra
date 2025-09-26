from .algebra_core import AlgebraicAction
from ...expressions.variables import a,b


class difference_of_squares_(AlgebraicAction):
	def __init__(self, **kwargs):
		super().__init__(
			a**2 - b**2,
			(a+b)*(a-b),
			**kwargs
		)
