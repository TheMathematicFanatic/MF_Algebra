from ..action_core import Action, IncompatibleExpression
from ...expressions.variables import Variable
from ...expressions.functions import Function
from ...utils import Smarten


class AlgebraicAction(Action):
	def __init__(self, template1, template2, var_condition_dict={}, var_kwarg_dict={}, extra_addressmaps=[], **kwargs):
		super().__init__(**kwargs)
		self.template1 = Smarten(template1)
		self.template2 = Smarten(template2)
		self.var_condition_dict = var_condition_dict #{c: lambda exp: isinstance(exp, Number)}
		self.var_kwarg_dict = var_kwarg_dict #{a:{"path_arc":PI}}
		self.extra_addressmaps = extra_addressmaps
		self.addressmap = None

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		var_dict = match_expressions(self.template1, input_expression, self.var_condition_dict)
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
		variables = self.get_all_variables()
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
		result = self.copy()
		result.template1, result.template2 = result.template2, result.template1
		return result

	def get_all_variables(self):
		return self.template1.get_all_variables() | self.template2.get_all_variables()




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
		if template.is_identical_to(expression):
			return {}
		raise IncompatibleExpression("Expressions do not match")
	
	# Node case
	var_dict = {}
	if not isinstance(expression, type(template)):
		raise IncompatibleExpression("Expressions do not match type")
	if not len(template.children) == len(expression.children):
		raise IncompatibleExpression("Expressions do not match children length")
	for tc,ec in zip(template.children, expression.children):
		child_dict = match_expressions(tc, ec, condition_dict)
		matching_keys = child_dict.keys() & var_dict.keys()
		if any(not child_dict[key].is_identical_to(var_dict[key]) for key in matching_keys):
			raise IncompatibleExpression("Conflicting matches for " + str(matching_keys))
		var_dict.update(child_dict)

	return var_dict



