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

	def __str__(self):
		symbol_string = self.get_symbol_string()
		argument_string = str(self.children[0]) if len(self.children) > 0 else ""
		return symbol_string + self.spacing + '{' + argument_string + '}'
	
	def get_symbol_string(self):
		# Overwrite for subclasses with indices, subscripts, etc
		return self.symbol

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


from .sequences import Sequence
class _OldFunction(Expression):
	def __init__(self, symbol, symbol_glyph_length, rule=None, algebra_rule=None, parentheses_mode="always", **kwargs):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.rule = rule #callable
		self.children = [Sequence()] # First child is always a sequence of arguments, further children are parameters like subscripts or indices
		self.algebra_rule = algebra_rule #SmE version of rule?
		self.parentheses_mode = parentheses_mode
		self.spacing = ""
		super().__init__(**kwargs)

	def __str__(self):
		return self.symbol + self.spacing + (str(self.children[0]) if len(self.children) > 0 else "")

	def __call__(self, *inputs, **kwargs):
		assert len(self.children[0].children) == 0, f"Function {self.symbol} cannot be called because it already has children."
		new_func = self.copy()
		new_func.children[0].children = list(map(Smarten, inputs))
		# have to reinitialize Expression and MathTex after setting children for correct indexing and auto_paren.
		Expression.__init__(self, parentheses = self.parentheses)
		return new_func
	
	@property
	def arguments(self):
		return self.children[0].children
	
	def set_spacing(self, spacing):
		self.spacing = spacing
		return self
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return
		child = self.children[0] #sequence
		if len(child.children) == 0:
			return
		if self.parentheses_mode == "always":
			child.give_parentheses(True)
		elif self.parentheses_mode in ["weak", "strong"]:
			from ..expressions.operations import Operation, Add, Sub
			if len(child.children) > 1:
				child.give_parentheses(True)
			elif isinstance(child.children[0], (Add, Sub)):
				child.give_parentheses(True)
			else:
				if self.parentheses_mode == "strong":
					if isinstance(child.children[0], Operation):
						child.give_parentheses(True)
		elif self.parentheses_mode == "never":
			child.give_parentheses(False)
		else:
			raise ValueError(f"Unsupported parentheses mode {self.parentheses_mode}.")
		
	def compute(self, *args):
		if len(args) == 0:
			return self.rule(*map(lambda exp: exp.compute(), self.children[0].children))
		else:
			return self.rule(*args)
	
    #def __pow__(self, other):
    # Gotta do something about sin^2 etc   

