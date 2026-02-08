from ..actions.action_core import Action, IncompatibleExpression
from ..expressions.variables import Variable
from ..expressions.functions import Function
from ..utils import Smarten
from MF_Tools.dual_compatibility import Write, FadeIn, FadeOut
from copy import deepcopy
from itertools import product


class AlgebraicAction(Action):
	template1 = None
	template2 = None
	addressmap = []
	auto_addressmap = True
	var_condition_dict = {}       # Example {c: lambda exp: isinstance(exp, Number)}
	var_kwarg_dict = {}           # Example {a:{'path_arc':PI}}

	def __init__(self,
		template1=None,
		template2=None,
		*extra_addressmaps,
		var_condition_dict={},
		var_kwarg_dict={},
		auto_addressmap=True,
		**kwargs
	):
		super().__init__(**kwargs)
		self.template1 = Smarten(self.template1) or Smarten(template1)
		self.template2 = Smarten(self.template2) or Smarten(template2)
		self.addressmap = self.addressmap or list(extra_addressmaps)
		self.var_condition_dict = self.var_condition_dict or var_condition_dict
		self.var_kwarg_dict = self.var_kwarg_dict or var_kwarg_dict
		self.auto_addressmap = self.auto_addressmap or auto_addressmap

	def get_output_expression(self, input_expression=None):
		var_dict = match_expressions(self.template1, input_expression, self.var_condition_dict)
		return self.template2.substitute(var_dict)

	def get_addressmap(self, input_expression=None):
		addressmap = [] if self.addressmap is None else list(self.addressmap)

		for i,entry in enumerate(addressmap):
			if entry[0] == [] and len(entry) == 2:
				addressmap[i] = [entry[0], entry[1], self.introduce_kwargs]
			elif entry[1] == [] and len(entry) == 2:
				addressmap[i] = [entry[0], entry[1], self.remove_kwargs]

		if not self.auto_addressmap:
			return addressmap

		def get_var_ad_dict(template):
			return {var: template.get_addresses_of_subex(var) for var in template.get_all_variables()}
		self.template1_address_dict = get_var_ad_dict(self.template1)
		self.template2_address_dict = get_var_ad_dict(self.template2)

		leaves = self.get_all_leaves()
		for leaf in leaves:
			kwargs = self.var_kwarg_dict.get(leaf, {})
			template1_addresses = self.template1_address_dict.get(leaf, [])
			template2_addresses = self.template2_address_dict.get(leaf, [])

			# print('leaves: ', leaves)
			# print('leaf: ', leaf)
			# print('template1_addresses: ', template1_addresses)
			# print('template2_addresses: ', template2_addresses)

			for t1ad, t2ad in product(template1_addresses, template2_addresses):
				if not any((t1ad, t2ad) == (str(ad[0]).strip('(_)'), str(ad[1]).strip('(_)')) for ad in addressmap):
					addressmap += [[t1ad, t2ad, kwargs]]
		
		return addressmap

	def __repr__(self):
		return f'AlgebraicAction({self.template1}, {self.template2})'
	
	def get_animation(self, *args, **kwargs):
		return super().get_animation(*args, auto_fade=True, auto_resolve_delay=0.1, **kwargs)

	def reverse(self):
		# swaps input and output templates
		result = self.copy()
		result.template1, result.template2 = result.template2, result.template1
		if result.addressmap is None:
			return result
		new_addressmap = deepcopy(result.addressmap)
		for entry in new_addressmap:
			entry[0], entry[1] = entry[1], entry[0]
			if len(entry) == 3 and 'path_arc' in entry[2].keys():
				entry[2]['path_arc'] = -entry[2]['path_arc']
			if entry[0] is FadeOut:
				entry[0] = self.introducer
			if entry[1] in (FadeIn, Write):
				entry[1] = self.remover
		result.addressmap = new_addressmap
		return result

	def get_all_variables(self):
		return self.template1.get_all_variables() | self.template2.get_all_variables()

	def get_all_leaves(self):
		return self.template1.get_all_leaves() | self.template2.get_all_leaves()

	def get_equation(self):
		assert self.template1 and self.template2
		from ..expressions.combiners.relations import Equation
		return Equation(self.template1, self.template2)



def match_expressions(template, expression, condition_dict={}):
	"""
		This function will either return a ValueError if the expression
		simply does not match the structure of the template, such as a missing
		operand or a plus in place of a times, or if they do match it will return
		a dictionary of who's who. For example,
		
		template:      (a*b)**n
		expression:    (4*x)**(3+y)
		return value:  {a:4, b:x, n:3+y}

		template:      n + x**5
		expression:    12 + x**3
		return value:  ValueError("Structures do not match at address 11, 5 vs 3")
		
		template:      x**n*x**m
		expression:    2**2*3**3
		return value:  ValueError("Conflicting matches for x: 2 and 3")

		Obviously this has to be recursive, but gee I am feeling a bit challenged atm...
		...
		Ok I think I've done it!
	"""
	# Leaf case
	if not template.children:
		condition = condition_dict.get(template, lambda exp: True)
		if not condition(expression):
			raise IncompatibleExpression(f"The subexpression {expression} is trying to match with {template}, but does not meet its given condition")
		if isinstance(template, Variable):
			return {template: expression}
		if isinstance(template, Function) and expression.is_function():
			return {template: expression}
		if template == expression:
			return {}
		raise IncompatibleExpression("Expressions do not match")
	
	# Node case
	var_dict = {}
	if not isinstance(expression, type(template)):
		raise IncompatibleExpression(f"Expressions do not match type: {expression} vs {template}")
	if not len(template.children) == len(expression.children):
		raise IncompatibleExpression("Expressions do not match children length")
	for tc,ec in zip(template.children, expression.children):
		child_dict = match_expressions(tc, ec, condition_dict)
		matching_keys = child_dict.keys() & var_dict.keys()
		if any(not child_dict[key] == var_dict[key] for key in matching_keys):
			raise IncompatibleExpression("Conflicting matches for " + str(matching_keys))
		var_dict.update(child_dict)

	return var_dict



