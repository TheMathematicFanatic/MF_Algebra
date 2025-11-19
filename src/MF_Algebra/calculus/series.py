from ..expressions.functions import ApplyFunction
from ..expressions.functions.operators import Sum
from ..expressions.variables import n,k,x
from .infinity import inf


class Series(ApplyFunction):
	def __init__(self,
		general_term,
		variable = n,
		start = 0,
		end = inf,
		**kwargs
	):
		variables = general_term.get_all_variables()
		if variable not in variables and len(variables) > 0:
			variable = variables.pop()
		self.variable = variable
		self.start = start
		self.end = end
		self.term = general_term
		self.sigma = Sum(variable, start, end)
		super().__init__(self.sigma, self.term, **kwargs)



