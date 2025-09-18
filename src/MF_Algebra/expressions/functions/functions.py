from ..expression_core import *
from ..combiners.sequences import Sequence
from ..combiners.operations import BinaryOperation
from ..variables import Variable


arg = Variable('arg')
c0 = Variable('c').subscript(0)
c1 = Variable('c').subscript(1)
c2 = Variable('c').subscript(2)
c3 = Variable('c').subscript(3)
c4 = Variable('c').subscript(4)


class ApplyFunction(BinaryOperation):
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function()
		self.eval_op = lambda x,y: x.__call__(x,y) # ???
		super().__init__('', 0, *children, **kwargs)
	
	@property
	def func(self):
		return self.children[0]

	@property
	def arg(self):
		return self.children[1]
	
	@Expression.parenthesize_latex
	def __str__(self):
		if hasattr(self.func, 'get_string_with_arg'):
			result = self.func.get_string_with_arg(self.arg)
			if result is not None:
				return result
		return super().__str__()

	def auto_parentheses(self):
		from ..combiners.combiners import Combiner
		if isinstance(self.func, Combiner): # Usually False, true for say (f+g)(x)
			self.func.give_parentheses(True)
		self.func.auto_parentheses()

		parentheses_mode = getattr(self.func, 'parentheses_mode', 'always')
		if parentheses_mode == 'always':
			self.arg.give_parentheses(True)
		from ..combiners.operations import Operation
		if parentheses_mode == 'strong' and isinstance(self.arg, Operation):
			self.arg.give_parentheses(True)
		from ..combiners.operations import Add, Sub
		if parentheses_mode == 'weak' and (isinstance(self.arg, (Add, Sub)) or self.arg.is_negative()):
			self.arg.give_parentheses(True)
		if parentheses_mode == 'never':
			self.arg.give_parentheses(False)
		self.arg.auto_parentheses()

		return self

	def is_function(self):
		# This should always be False because it can no longer be called on something
		# Maybe not in very bold circumstances, but this will do for now
		return False



class Function(Expression):
	def __init__(self,
		symbol = None,
		symbol_glyph_length = None,
		python_rule = None,
		algebra_rule_variables = [],
		algebra_rule = None,
		parentheses_mode = "always",
		children = [],
		# First child is argument(s) such as a Variable, Number, or Sequence.
		# Further children are parameters like subscripts, indices, or bounds.
		# First child needs to have a placeholder if not filled so that indices etc can be added before the main argument.
		**kwargs
	):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.python_rule = python_rule #callable
		self.algebra_rule_variables = algebra_rule_variables
		self.algebra_rule = algebra_rule
		self.parentheses_mode = parentheses_mode
		super().__init__(children=children, **kwargs)
	
	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return self.symbol_glyph_length

	@Expression.parenthesize_latex
	def __str__(self):
		return self.get_symbol_string()

	def get_string_with_arg(self, arg):
		return None

	def get_symbol_string(self):
		return self.symbol
	
	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'f': 'get_main_func_glyphs',
		'F': 'get_all_func_glyphs',
	}

	def get_main_func_glyphs(self):
		return list(range(0, self.symbol_glyph_length))

	def get_all_func_glyphs(self):
		return list(range(0, self.symbol_glyph_length))

	def get_glyphs_at_addigit(self, addigit):
		raise NotImplementedError

	def is_function(self):
		return True
	
	def is_identical_to(self, other):
		return super().is_identical_to(other) and self.get_symbol_string() == other.get_symbol_string()




class _AbsoluteValue(Function):
	string_code = ['\\left|', arg, '\\right|']
	glyph_code = [1, arg, 1]

class _Radical(Function):
	string_code = ['\\sqrt[', c0, ']', arg]
	glyph_code = [c0, 2, arg]

class _Logarithm(Function):
	string_code = ['\\log', c0, arg]
	glyph_code = [3, c0, arg]

class _Factorial(Function):
	string_code = [arg, '!']
	glyph_code = [arg, 1]


class Composition(BinaryOperation):
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function() and children[1].is_function()
		self.eval_op = lambda x,y: Expression.__call__(x,y) # ???
		super().__init__('\\circ', 1, *children, **kwargs)











class _OldFunction(Expression):
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
		count = 0
		if self.symbol and self.symbol_glyph_length:
			count += self.symbol_glyph_length
		count += self.arg.glyph_count
		return count

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
			end = start + self.arg.glyph_count
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
		if self.arg.is_identical_to(Sequence()):
			return self
		if self.parentheses_mode == 'always' or isinstance(self.arg, Sequence):
			self.arg.give_parentheses(True)
			return self
		from ..combiners.operations import BinaryOperation, Add, Sub
		from .functions import Function
		if self.parentheses_mode == 'strong' and isinstance(self.arg, (BinaryOperation, Function)):
			self.arg.give_parentheses(True)
		if self.parentheses_mode == 'weak' and isinstance(self.arg, (Add, Sub)):
			self.arg.give_parentheses(True)
		if self.parentheses_mode == 'never':
			self.arg.give_parentheses(False)
		return self
	
	def compute(self):
		if self.arg.is_identical_to(Sequence()):
			raise ValueError(f"Function {self.symbol} has no arguments.")
		if isinstance(self.arg, Sequence):
			args = self.arg.children
		else:
			args = [self.arg]
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
