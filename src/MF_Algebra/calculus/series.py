from ..expressions.functions import Function, ApplyFunction, Sum, fact
from ..expressions.variables import n,k,x

from .limits import inf


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



from ..trigonometry import sin, cos
from ..expressions import e, x, n, fact
class Taylor(Series):
	def __init__(self, func, var=x, center=0, **kwargs):
		if center != 0: raise NotImplementedError
		if isinstance(func, Function):
			func = func(x)
		term = self.term_from_func[func]
		super().__init__(term)
	
	term_from_func = {
		sin(x)  : ((-1)**n * x**fact(2*n+1))/fact(2*n+1),
		cos(x)  : ((-1)**n * x**fact(2*n))/fact(2*n),
		e**x    : x**n / fact(n),
		1/(1-x) : x**n
	}
	



