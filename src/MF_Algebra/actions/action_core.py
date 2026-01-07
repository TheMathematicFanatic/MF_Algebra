from ..expressions.expression_core import Expression
from ..expressions.combiners.operations import Mul
from .animations import TransformByAddressMap
from MF_Tools.dual_compatibility import Write, FadeIn, FadeOut, TransformMatchingTex
from ..utils import MF_Base, apply_addressmap
from functools import wraps


class Action(MF_Base):
	introducer = Write
	introduce_kwargs = {'run_time':0.5, 'delay':0.5}
	remover = FadeOut
	remove_kwargs = {'run_time':0.5}
	preaddress = ''
	def __init__(self,
		introducer=None,
		remover=None,
		preaddress=''
	):
		self.introducer = introducer or self.introducer
		self.remover = remover or self.remover
		self.preaddress = preaddress or self.preaddress

	def get_output_expression(self, input_expression):
  		# define in subclasses
		return None

	def get_addressmap(self, input_expression, **kwargs):
		# define in subclasses
		return [['', '']]


	### Animating ###

	def get_animation(self, **kwargs):
		def animation(input_exp, output_exp=None, **kwargs):
			if output_exp is None:
				output_exp = self.get_output_expression(input_exp)
			def get_TBAM(action, input_exp, output_exp, **kwargs):
				return TransformByAddressMap(
					input_exp,
					output_exp,
					*action.get_addressmap(input_exp),
					default_introducer=action.introducer,
					default_remover=action.remover,
					**kwargs
				)
			try:
				TBAM = get_TBAM(self.copy(), input_exp.copy(), output_exp.copy())
				assert not TBAM.show_indices, f'Invalid Glyphmap: {TBAM.glyphmap}'
				return get_TBAM(self, input_exp, output_exp)
			except Exception as E:
				print('Warning: Action produced an invalid glyphmap. Falling back to TransformMatchingTex')
				print('Exception: ', E)
				print('Action: ', self)
				print('Input: ', input_exp)
				print('Output: ', output_exp)
				print('Addressmap: ', self.get_addressmap(input_exp))
				return TransformMatchingTex(input_exp.mob, output_exp.mob, **kwargs)
		return animation

	def __call__(self, expr1, expr2=None, **kwargs):
		return self.get_animation(**kwargs)(expr1, expr2)


	### Modifiers ###

	def pread(self, *addresses, **kwargs):
		self = self.copy()
		if len(addresses) == 0:
			return self
		elif len(addresses) == 1:
			self.preaddress = addresses[0] + self.preaddress
			return self
		else:
			from .parallel import ParallelAction
			return ParallelAction(*[self.pread(ad) for ad in addresses], **kwargs)

	def left(self, **kwargs):
		return self.pread('0', **kwargs)

	def right(self, **kwargs):
		return self.pread('1', **kwargs)

	def both(self, number_of_children=2, **kwargs):
		# Intended to turn an action on an expression into an action done to both sides of an equation.
		# Can be passed a number to apply to more than 2 sides for, say, a triple equation or inequality.
		return self.pread(*[str(i) for i in range(number_of_children)], **kwargs)


	### Combinations ###

	def create_parallel(self, other):
		from .parallel import ParallelAction
		if isinstance(other, ParallelAction):
			return ParallelAction(self, *other.actions)
		elif isinstance(other, Action):
			return ParallelAction(self, other)
		else:
			raise ValueError("Can only use |,+ with other ParallelAction or Action")

	def __or__(self, other):
		return self.create_parallel(other)
	
	def __add__(self, other):
		return self.create_parallel(other)

	def __le__(self, expr):
		assert isinstance(expr, Expression), "Can only apply expression >= action"
		return self.get_output_expression(expr)


	### Decorators ###

	def __init_subclass__(cls):
		super().__init_subclass__()
		if not getattr(cls, '_is_decorated', False):
			cls._is_decorated = True

			func = cls.get_output_expression
			func = Action.preaddressfunc(func)
			cls.get_output_expression = func

			func = cls.get_addressmap
			func = Action.preaddressmap(func)
			func = Action.autoparenmap(func)
			func = Action.autoopmap(func)
			cls.get_addressmap = func


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
		if mode == 'none':
			return getmap
		if mode == 'stupid':
			@wraps(getmap)
			def wrapper(action, expr, *args, **kwargs):
				addressmap = list(getmap(action, expr, *args, **kwargs))
				in_expr, out_expr = expr, action.get_output_expression(expr)
				for in_add in in_expr.get_all_addresses():
					if in_expr.get_subex(in_add).parentheses:
						addressmap.append([in_add+'()', [], Action.remove_kwargs.copy()])
					for entry in addressmap:
						if entry[0] == in_add:
							entry[0] = entry[0] + '_'
				for out_add in out_expr.get_all_addresses():
					if out_expr.get_subex(out_add).parentheses:
						addressmap.append([[], out_add+'()', Action.introduce_kwargs.copy()])
					for entry in addressmap:
						if entry[1] == out_add:
							entry[1] = entry[1] + '_'
				return addressmap

		if mode == 'smart':
			@wraps(getmap)
			def wrapper(action, expr, *args, **kwargs):
				addressmap = list(getmap(action, expr, *args, **kwargs))
				in_expr, out_expr = expr, action.get_output_expression(expr)
		return wrapper

	@staticmethod
	def autoopmap(getmap, ops_to_check=(Mul,)):

		@wraps(getmap)
		def wrapper(action, expr:Expression, *args, **kwargs):

			addressmap = list(getmap(action, expr, *args, **kwargs))
			in_ads = [entry[0] for entry in addressmap]
			out_ads = [entry[1] for entry in addressmap]

			in_expr, out_expr = expr, action.get_output_expression(expr)
			in_op_ads = in_expr.get_all_addresses_of_type(ops_to_check)
			out_op_ads = out_expr.get_all_addresses_of_type(ops_to_check)

			for ad in in_op_ads:
				
				if any(ad + op in in_ads for op in '+-*/^=<>,'):
					# If op explicitly handled, abort
					continue

				targets = apply_addressmap(ad, addressmap)

				if targets is None or len(targets) != 1:
					# Ambiguous addressmap, just fade out
					addressmap.append( [ad + '+', [], Action.remove_kwargs.copy()] )
				
				# elif len(targets) == 0:
				# 	pass #idk what im doing

				else:
					# Matching address found
					target = targets.pop()
					in_len = in_expr.get_subex(ad).symbol_glyph_length

					if target in out_op_ads:
						# Matching address is also a checked type (??)
						out_op_ads.remove(target)
						out_len = out_expr.get_subex(target).symbol_glyph_length
					else:
						# Idk I'm a bit confused here
						continue

					if in_len and out_len:
						# Both are checked type and have op glyphs, map to each other
						addressmap.append( [ad + '+', target + '+'] )
					
					elif in_len and not out_len:
						# Fade out glyph
						addressmap.append( [ad + '+', [], Action.remove_kwargs.copy()])
					
					elif not in_len and out_len:
						# Fade in glyph
						addressmap.append( [[], target + '+', Action.introduce_kwargs.copy()])
					
					else:
						# Neither has glyph so ignore
						pass
			
			for ad in out_op_ads:

				if any(ad + op in out_ads for op in '+-*/^=<>,'):
					continue

				targets = apply_addressmap(ad, addressmap, reverse=True)

				if targets is None or len(targets) != 1:
					addressmap.append( [[], ad + '+', Action.introduce_kwargs.copy()] )
				
				else:
					raise Exception('This case should have already been caught in the in_op_ads loop.')
			
			return addressmap

		return wrapper





	### Utilities ###

	def __repr__(self):
		max_length = 50
		string = type(self).__name__ + '(' + self.preaddress + ')'
		if len(string) > max_length:
			string = string[:max_length-3] + '...'
		return string



class IncompatibleExpression(Exception):
	pass



