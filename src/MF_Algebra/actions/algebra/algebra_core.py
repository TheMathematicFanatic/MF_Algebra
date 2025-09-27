from ..action_core import Action
from ...utils import match_expressions


class AlgebraicAction(Action):
	def __init__(self, template1, template2, var_kwarg_dict={}, extra_addressmaps=[], **kwargs):
		super().__init__(**kwargs)
		self.template1 = template1
		self.template2 = template2
		self.var_kwarg_dict = var_kwarg_dict #{a:{"path_arc":PI}}
		self.extra_addressmaps = extra_addressmaps
		self.addressmap = None

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		var_dict = match_expressions(self.template1, input_expression)
		return self.template2.substitute(var_dict)

	@Action.autoparenmap
	@Action.preaddressmap
	def get_addressmap(self, input_expression=None):
		# Best overwritten in subclasses, but this gets the job done sometimes.
		# Actually, I think most subclasses will have a static addressmap, so I'll add this line at the start.
		if self.addressmap is not None:
			return self.addressmap

		addressmap = []
		def get_var_ad_dict(template):
			return {var: template.get_addresses_of_subex(var) for var in template.get_all_variables()}
		self.template1_address_dict = get_var_ad_dict(self.template1)
		self.template2_address_dict = get_var_ad_dict(self.template2)
		variables = self.template1_address_dict.keys() | self.template2_address_dict.keys()
		for var in variables:
			kwargs = self.var_kwarg_dict.get(var, {})
			if len(self.template1_address_dict[var]) == 1:
				addressmap += [
					[self.template1_address_dict[var][0], t2ad, kwargs]
					for t2ad in self.template2_address_dict[var]
				]
			elif len(self.template2_address_dict[var]) == 1:
				addressmap += [
					[t1ad, self.template2_address_dict[var][0], kwargs]
					for t1ad in self.template1_address_dict[var]
				]
			else:
				raise ValueError("I don't know what to do when a variable appears more than once on both sides. Please set addressmap manually.")
		addressmap += self.extra_addressmaps
		return addressmap

	def __repr__(self):
		return f'AlgebraicAction({self.template1}, {self.template2})'
	
	# def get_animation(self, *args, **kwargs):
	#     return super().get_animation(*args, auto_fade=True, auto_resolve_delay=0.1, **kwargs)

	def reverse(self):
		# swaps input and output templates
		self.template1, self.template2 = self.template2, self.template1
		return self








