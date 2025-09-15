from .expression_core import *
from .sequences import Sequence
from .numbers import Integer, e
import numpy as np


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
		from ..expressions.operations import BinaryOperation, Add, Sub
		from ..expressions.functions import Function
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


class Rad(Function):
	def __init__(self, index, allow_nickname = True, **kwargs):
		super().__init__(
			parentheses_mode = 'never',
			**kwargs
        )
		index = Smarten(index)
		self.children.append(index)
		if index.is_identical_to(Integer(2)) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\sqrt'
		else:
			self.nicknamed = False
			self.symbol = f'\\sqrt[{index}]'
	
	@property
	def index(self):
		return self.children[1]

	def get_symbol_string(self):
		if self.nicknamed:
			return '\\sqrt'
		return f'\\sqrt[{self.index}]'

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return self.index_glyph_count() + self.radical_glyph_count() + self.children[0].glyph_count

	def index_glyph_count(self):
		if self.nicknamed:
			return 0
		else:
			return self.index.glyph_count

	def radical_glyph_count(self):
		if algebra_config['fast_root_length']:
			return 2
		else:
			raise NotImplementedError

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		if addigit == 0:
			start += self.index_glyph_count()
			start += self.radical_glyph_count()
			end = start + self.children[0].glyph_count
			return list(range(start, end))
		elif addigit == 1:
			end = start + self.index_glyph_count()
			return list(range(start, end))

	def get_func_glyphs_with_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		end = start + self.index_glyph_count()
		end += self.radical_glyph_count()
		return list(range(start, end))

	def get_func_glyphs_without_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		start += self.index_glyph_count()
		end = start + self.radical_glyph_count()
		return list(range(start, end))


sqrt = Rad(2)

cbrt = Rad(3)



class Log(Function):
	def __init__(self, base, allow_nickname = True, **kwargs):
		super().__init__(
			parentheses_mode = 'weak',
			**kwargs
        )
		base = Smarten(base)
		self.children.append(base)
		if base.is_identical_to(Integer(10)) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\log'
			self.symbol_glyph_length = 3
		elif base.is_identical_to(e) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\ln'
			self.symbol_glyph_length = 2
		else:
			self.nicknamed = False
			self.symbol = f'\\log_{base}'

	@property
	def base(self):
		return self.children[1]

	def get_symbol_string(self):
		if self.nicknamed:
			if self.base.is_identical_to(Integer(10)):
				return '\\log'
			elif self.base.is_identical_to(e):
				return '\\ln'
		return '\\log_{' + str(self.base) + '}'

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if self.nicknamed:
			return self.symbol_glyph_length
		return self.base_glyph_count() + self.log_glyph_count() + self.arg.glyph_count

	def base_glyph_count(self):
		if self.nicknamed:
			return 0
		else:
			return self.base.glyph_count

	def log_glyph_count(self):
		if self.nicknamed and self.base.is_identical_to(e):
			return 2
		else:
			return 3

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		if addigit == 0:
			start += self.base_glyph_count()
			start += self.log_glyph_count()
			end = start + self.arg.glyph_count
			return list(range(start, end))
		elif addigit == 1:
			start += self.log_glyph_count()
			end = start + self.base_glyph_count()
			return list(range(start, end))

	def get_func_glyphs_with_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		end = start + self.base_glyph_count()
		end += self.log_glyph_count()
		return list(range(start, end))

	def get_func_glyphs_without_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		start += self.base_glyph_count()
		end = start + self.log_glyph_count()
		return list(range(start, end))


ln = Log(e)
