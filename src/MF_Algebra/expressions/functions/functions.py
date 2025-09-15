from ..expression_core import *
from ..combiners.sequences import Sequence


class Function(Expression):
	def __init__(self,
		symbol = None,
		symbol_glyph_length = None,
		python_rule = None,
		algebra_rule_variables = [],
		algebra_rule = None,
		parentheses_mode="always",
		spacing = "",
		children=[Sequence()],
		# First child is argument(s) such as a Variable, Number, or Sequence.
		# Further children are parameters like subscripts, indices, or bounds.
		# First child needs to have a placeholder if not filled so that indices etc can be added before the main argument.
		**kwargs
	):
		self.parentheses_mode = parentheses_mode
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.python_rule = python_rule #callable
		self.algebra_rule_variables = algebra_rule_variables
		self.algebra_rule = algebra_rule
		self.spacing = spacing
		super().__init__(children=children, **kwargs)

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if self.symbol and self.symbol_glyph_length:
			return self.symbol_glyph_length

	@Expression.parenthesize_latex
	def __str__(self):
		symbol_string = self.get_symbol_string()
		argument_string = str(self.arg)
		return symbol_string + self.spacing + '{' + argument_string + '}'
	
	def get_symbol_string(self):
		# Overwrite for subclasses with indices, subscripts, etc
		return self.symbol

	@property
	def arg(self):
		return self.children[0]

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'F': 'get_func_glyphs_with_extras',
		'f': 'get_func_glyphs_without_extras',
	}

	def get_glyphs_at_addigit(self, addigit:int):
		# Overwrite for subclasses with indices, subscripts, etc
		if addigit == 0:
			start = self.symbol_glyph_length
			start += self.parentheses * self.paren_length()
			end = start + self.children[0].glyph_count
			return list(range(start, end))
		else:
			raise NotImplementedError(f"This function has no children at index {addigit}")
	
	def get_func_glyphs_with_extras(self):
		return list(range(0, self.symbol_glyph_length))
	
	def get_func_glyphs_without_extras(self):
		return list(range(0, self.symbol_glyph_length))
	
	def __call__(self, *inputs):
		new_func = self.copy()
		if len(inputs) == 1:
			new_child = Smarten(inputs[0])
		elif len(inputs) > 1:
			new_child = Sequence(*list(map(Smarten, inputs)))
		new_func.children[0] = new_child
		new_func.auto_parentheses()
		new_func._mob = None
		new_func._glyph_count = None
		return new_func
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return self
		if self.parentheses_mode == 'always' or isinstance(self.children[0], Sequence) and not self.children[0].is_identical_to(Sequence()):
			self.children[0].give_parentheses(True)
			return self
		from ..combiners.operations import BinaryOperation, Add, Sub
		from .functions import Function
		if self.parentheses_mode == 'strong' and isinstance(self.children[0], (BinaryOperation, Function)):
			self.children[0].give_parentheses(True)
		if self.parentheses_mode == 'weak' and isinstance(self.children[0], (Add, Sub)):
			self.children[0].give_parentheses(True)
		if self.parentheses_mode == 'never':
			self.children[0].give_parentheses(False)
		return self
	
	def compute(self):
		if self.arg.is_identical_to(Sequence()):
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


f = Function('f', 1)

g = Function('g', 1)

h = Function('h', 1)
