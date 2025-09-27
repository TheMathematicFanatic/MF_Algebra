from ..expressions.expression_core import Expression
from .animations import TransformByAddressMap
from MF_Tools.dual_compatibility import Write, FadeIn, FadeOut
from ..utils import MF_Base
from functools import wraps

class Action(MF_Base):
	def __init__(self,
		introducer=Write,
		remover=FadeOut,
		preaddress=''
	):
		self.introducer = introducer
		self.remover = remover
		self.preaddress = preaddress

	def get_output_expression(self, input_expression):
  		# define in subclasses
		raise NotImplementedError

	def get_addressmap(self, input_expression, **kwargs):
		# define in subclasses
		raise NotImplementedError

	def get_animation(self, **kwargs):
		def animation(input_exp, output_exp=None):
			if output_exp is None:
				output_exp = self.get_output_expression(input_exp)
			return TransformByAddressMap(
			input_exp,
			output_exp,
			*self.get_addressmap(input_exp),
			default_introducer=self.introducer,
			default_remover=self.remover,
			**kwargs
			)
		return animation

	def __call__(self, expr1, expr2=None, **kwargs):
		return self.get_animation(**kwargs)(expr1, expr2)

	def __or__(self, other):
		from .parallel import ParallelAction
		if isinstance(other, ParallelAction):
			return ParallelAction(self, *other.actions)
		elif isinstance(other, Action):
			return ParallelAction(self, other)
		else:
			raise ValueError("Can only use | with other ParallelAction or Action")

	def __repr__(self):
		max_length = 50
		string = type(self).__name__ + "(" + self.preaddress + ")"
		if len(string) > max_length:
			string = string[:max_length-3] + '...'
		return string

	def both(self, number_of_sides=2):
		# Intended to turn an action on an expression into an action done to both sides of an equation.
		# Can be passed a number to apply to more than 2 sides for, say, a triple equation or inequality.
		return self.pread(*[str(i) for i in range(number_of_sides)])

	def pread(self, *addresses):
		if len(addresses) == 0:
			return self
		elif len(addresses) == 1:
			self.preaddress = addresses[0] + self.preaddress
			return self
		else:
			from .parallel import ParallelAction
			return ParallelAction(*[self.copy().pread(ad) for ad in addresses])

	def __le__(self, expr):
		assert isinstance(expr, Expression), "Can only apply expression >= action"
		return self.get_output_expression(expr)

	@staticmethod
	def preaddressfunc(func):
		@wraps(func)
		def wrapper(action, expr, *args, **kwargs):
			expr = expr.copy()
			preaddress = kwargs.get('preaddress', '') or action.preaddress
			active_part = expr.get_subex(preaddress)
			result = func(action, active_part)
			output_expression = expr.substitute_at_address(result, preaddress)
			output_expression.reset_parentheses()
			return output_expression
		return wrapper

	@staticmethod
	def preaddressmap(getmap):
		@wraps(getmap)
		def wrapper(action, expr, *args, **kwargs):
			expr = expr.copy()
			preaddress = kwargs.get('preaddress', '') or action.preaddress
			addressmap = getmap(action, expr, *args, **kwargs)
			if preaddress:
				for entry in addressmap:
					for i, ad in enumerate(entry):
						if isinstance(ad, str):
							entry[i] = preaddress + ad
			return addressmap
		return wrapper

	@staticmethod
	def autoparenmap(getmap, mode='stupid'):
		if mode=='stupid':
			@wraps(getmap)
			def wrapper(action, expr, *args, **kwargs):
				addressmap = list(getmap(action, expr, *args, **kwargs))
				in_expr, out_expr = expr, action.get_output_expression(expr)
				for in_add in in_expr.get_all_addresses():
					if in_expr.get_subex(in_add).parentheses:
						addressmap.append([in_add+'()', FadeOut, {'run_time':0.5}])
					for entry in addressmap:
						if entry[0] == in_add:
							entry[0] = entry[0] + '_'
				for out_add in out_expr.get_all_addresses():
					if out_expr.get_subex(out_add).parentheses:
						addressmap.append([FadeIn, out_add+'()', {'run_time':0.5, 'delay':0.5}])
					for entry in addressmap:
						if entry[1] == out_add:
							entry[1] = entry[1] + '_'
				return addressmap

		if mode=='smart':
			@wraps(getmap)
			def wrapper(action, expr, *args, **kwargs):
				addressmap = list(getmap(action, expr, *args, **kwargs))
				in_expr, out_expr = expr, action.get_output_expression(expr)
		return wrapper


class IncompatibleExpression(Exception):
	pass
