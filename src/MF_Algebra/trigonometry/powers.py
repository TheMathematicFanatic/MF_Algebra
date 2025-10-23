from .trigonometry_core import TrigFunction
from ..expressions.combiners.operations import Pow


class TrigPower(Pow, TrigFunction):
	def expand_on_args(self, *arg_expressions):
		return self.left(*arg_expressions)**self.right





