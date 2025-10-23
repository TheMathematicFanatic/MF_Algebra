from .action_core import Action
from ..expressions.expression_core import Expression
from MF_Tools.dual_compatibility import PI, DOWN, FadeIn, FadeOut




class substitute_(Action):
	def __init__(self,
		sub_dict,
		mode = 'transform',
		arc_size = PI,
		fade_shift = DOWN*0.2,
		lag = 0,
		maintain_color = False,
		**kwargs
	):
		self.sub_dict = sub_dict
		self.mode = mode
		self.arc_size = arc_size
		self.fade_shift = fade_shift
		self.lag = lag #usually looks like shit but can be cool sometimes
		self.maintain_color = maintain_color
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		result = input_expression.substitute(self.sub_dict)
		if self.maintain_color:
			for from_subex, to_subex in self.sub_dict.items():
				color = input_expression.get_color_of_subex(from_subex)
				addresses = input_expression.get_addresses_of_subex(from_subex)
				result[*addresses].set_color(color)
		return result

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression=None):
		target_addresses = []
		for var in self.sub_dict:
			target_addresses += input_expression.get_subex(self.preaddress).get_addresses_of_subex(var)
		addressmap = []
		if self.mode == "transform":
			for i,ad in enumerate(target_addresses):
				addressmap.append([ad, ad, {"delay": self.lag*i}])
		elif self.mode == "swirl":
			for i,ad in enumerate(target_addresses):
				addressmap.append([ad, ad, {"path_arc": self.arc_size, "delay": self.lag*i}])
		elif self.mode == "fade":
			for i,ad in enumerate(target_addresses):
				addressmap.append([ad, FadeOut, {"shift": self.fade_shift, "delay": self.lag*i}])
				addressmap.append([FadeIn, ad, {"shift": self.fade_shift, "delay": self.lag*i}])

		# Horrible bandaid for the problem of multiplication symbols changing and ruining the addressmap
		# I am certain that there is a general and elegant way to do this, along with parentheses changes,
		# and other such aesthetic matters which don't change the tree, but I still haven't figured it out.
		from ..expressions.combiners.operations import Mul
		input_expression = input_expression.copy()
		output_expression = self.get_output_expression(input_expression.copy())
		for ad in output_expression.get_all_addresses():
			in_subex = input_expression.get_subex(ad)
			out_subex = output_expression.get_subex(ad)
			if isinstance(in_subex, Mul) and isinstance(out_subex, Mul):
				if in_subex.symbol == '' and out_subex.symbol != '':
					addressmap.append([ad, ad+'*'])
				if in_subex.symbol != '' and out_subex.symbol == '':
					addressmap.append([ad+'*', ad])

		return addressmap
		
	def __repr__(self):
		return type(self).__name__ + "(" + str(self.sub_dict) + (',' + self.preaddress if self.preaddress else '') + ")"


class substitute_into_(Action):
	def __init__(self, outer_expression, substitution_variable=None, **kwargs):
		self.outer_expression = outer_expression
		if isinstance(substitution_variable, Expression) and substitution_variable.is_variable():
			self.substitution_variable = substitution_variable
		elif substitution_variable is None:
			exp_vars = outer_expression.get_all_variables()
			if len(exp_vars) == 1:
				self.substitution_variable = exp_vars.pop()
			else:
				raise ValueError('Substitution variable must be explicitly given if the expression does not have one variable')
		else:
			raise ValueError(f'Invalid value for substitution_variable: {substitution_variable}')
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		return self.outer_expression.substitute({self.substitution_variable: input_expression})

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression=None):
		sub_into_addresses = self.outer_expression.get_addresses_of_subex(self.substitution_variable)
		addressmap = [
			['', ad]
			for ad in sub_into_addresses
		]
		return addressmap
	
	def get_animation(self, *args, **kwargs):
		return super().get_animation(*args, auto_fade=True, auto_resolve_delay=0.75, **kwargs)
