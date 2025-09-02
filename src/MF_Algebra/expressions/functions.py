from .expression_core import *


class Function(Expression):
	def __init__(self,
		symbol,
		symbol_glyph_length = None,
		python_rule = None,
		algebra_rule_variables = [],
		algebra_rule = None,
		parentheses_mode="always",
		spacing = "",
		**kwargs
	):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.python_rule = python_rule #callable
		self.algebra_rule_variables = algebra_rule_variables
		self.algebra_rule = algebra_rule
		self.parentheses_mode = parentheses_mode
		self.spacing = spacing
		# First child is argument(s) such as a Variable, Number, or Sequence.
		# Further children are parameters like subscripts, indices, or bounds.
		self.children = []
		super().__init__(**kwargs)

	@parenthesize
	def __str__(self):
		symbol_string = self.get_symbol_string()
		argument_string = str(self.children[0]) if len(self.children) > 0 else ""
		return symbol_string + self.spacing + '{' + argument_string + '}'
	
	def get_symbol_string(self):
		# Overwrite for subclasses with indices, subscripts, etc
		return self.symbol

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'F': 'get_func_glyphs',
		'f': 'get_func_glyphs',
	}

	def get_glyphs_at_addigit(self, addigit):
		# Overwrite for subclasses with indices, subscripts, etc
		child_index = int(addigit)
		if child_index == 0:
			start = self.symbol_glyph_length
			start += self.parentheses * self.paren_length()
			end = start + self.children[0].number_of_glyphs()
			return list(range(start, end))
		else:
			raise NotImplementedError(f"This function has no children at index {addigit}")
	
	def get_func_glyphs(self):
		return list(range(0, self.symbol_glyph_length))
	
	def number_of_glyphs(self):
		result = self.symbol_glyph_length
		result += self.children[0].number_of_glyphs()
		result += self.parentheses * self.paren_length() * 2
		return result

	def __call__(self, *inputs):
		new_func = self.copy()
		if len(inputs) == 1:
			new_func.children.append(Smarten(inputs[0]))
		elif len(inputs) > 1:
			from .sequences import Sequence
			new_func.children.append(Sequence(*list(map(Smarten, inputs))))
		new_func.auto_parentheses()
		new_func._mob = None
		return new_func
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return self
		from ..expressions.sequences import Sequence
		if self.parentheses_mode == 'always' or isinstance(self.children[0], Sequence):
			self.children[0].give_parentheses(True)
			return self
		from ..expressions.operations import Operation, Add, Sub
		from ..expressions.functions import Function
		if self.parentheses_mode == 'strong' and isinstance(self.children[0], (Operation, Function)):
			self.children[0].give_parentheses(True)
		if self.parentheses_mode == 'weak' and isinstance(self.children[0], (Add, Sub)):
			self.children[0].give_parentheses(True)
		if self.parentheses_mode == 'never':
			self.children[0].give_parentheses(False)
		return self
	
	def compute(self):
		from ..expressions.sequences import Sequence
		if len(self.children) == 0:
			raise ValueError(f"Function {self.symbol} has no arguments.")
		if isinstance(self.children[0], Sequence):
			args = self.children[0].children
		else:
			args = [self.children[0]]
		args = [arg.compute() for arg in args]
		if self.python_rule is not None:
			return self.python_rule(*args)
		elif self.algebra_rule is not None:
			if self.algebra_rule_variables is not None:
				substituted_expression = self.algebra_rule.substitute({var:val for var, val in zip(self.algebra_rule_variables, args)})
			elif len(var_set := self.algebra_rule.get_all_variables()) == len(args) == 1:
				substituted_expression = self.algebra_rule.substitute({list(var_set):args[0]})
			else:
				raise ValueError(f"Algebra rule {self.algebra_rule} requires {len(self.algebra_rule_variables)} arguments, but {len(args)} were given.")
			return substituted_expression.compute()
