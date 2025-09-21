from ..expression_core import *
from ..combiners.sequences import Sequence
from ..combiners.operations import BinaryOperation
from ..variables import Variable


arg = Variable(f'arg')
child = lambda n: Variable(f'child {n}')
c0 = child(0)
c1 = child(1)
c2 = child(2)
c3 = child(3)
c4 = child(4)


# Example glyph and string codes

# Sigma
string_code = ['\\sum_{', c0, '}^{', c1, '}', arg]
glyph_code = [c1, 1, c0, arg]

# Nth Root
string_code = ['\\sqrt[', c0, ']{', arg, '}']
glyph_code = [c0, 2, arg]

# Default
string_code = [lambda self: self.symbol, arg]
glyph_code = [lambda self: self.symbol_glyph_length, arg]



class Function(Expression):
	string_code = [lambda self: self.symbol, arg]
	glyph_code = [lambda self: self.symbol_glyph_length, arg]
	def __init__(self,
		symbol = None,
		symbol_glyph_length = None,
		python_rule = None,
		algebra_rule_variables = [],
		algebra_rule = None,
		parentheses_mode = "always",
		children = [],
		**kwargs
	):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.python_rule = python_rule #callable
		self.algebra_rule_variables = algebra_rule_variables
		self.algebra_rule = algebra_rule
		self.parentheses_mode = parentheses_mode
		super().__init__(children=children, **kwargs)

	@Expression.parenthesize_latex
	def __str__(self):
		return self.get_string_from_code()

	def get_string_from_code(self, arg=''):
		string = ''
		for sc in self.string_code:
			if isinstance(sc, Variable) and sc.symbol == 'arg':
				string += arg
			else:
				string += self.str_from_string_code_entry(sc)
		return string

	def str_from_string_code_entry(self, entry):
		if isinstance(entry, str):
			return entry
		if isinstance(entry, Variable) and entry.symbol.startswith('child'):
			func_child_number = int(entry.symbol.split()[-1])
			return str(self.children[func_child_number])
		try:
			return entry(self)
		except:
			raise ValueError(f'Invalid glyph code entry of type {type(entry)}: {entry}')

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self): # Needs glyph_code rework
		return self.symbol_glyph_length

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		for gc in self.glyph_code:
			if isinstance(gc, Variable) and gc.symbol == 'arg':
				pass
			if isinstance(gc, Variable) and gc.is_identical_to(child(addigit)):
				end = start + self.children[addigit].glyph_count
				return list(range(start, end))
			else:
				start += self.int_from_glyph_code_entry(gc)
			return []

	def int_from_glyph_code_entry(self, entry):
		if isinstance(entry, int):
			return entry
		if isinstance(entry, Variable) and entry.symbol.startswith('child'):
			child_number = int(entry.symbol.split()[-1])
			return self.children[child_number].glyph_count
		if isinstance(entry, Variable) and entry.symbol == 'arg':
			raise ValueError('arg should not be processed by the child function')
		try:
			return entry(self)
		except:
			raise ValueError(f'Invalid glyph code entry of type {type(entry)}: {entry}')

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'f': 'get_main_func_glyphs',
		'F': 'get_all_func_glyphs',
	}

	def get_main_func_glyphs(self): # Needs glyph_code rework
		return list(range(0, self.symbol_glyph_length))

	def get_all_func_glyphs(self): # Needs glyph_code rework
		return list(range(0, self.symbol_glyph_length))

	def is_function(self):
		return True
	
	def is_identical_to(self, other):
		return super().is_identical_to(other) and str(self) == str(other)

	def compute(self):
		raise ValueError('Functions should not be computed directly. It can be computed on its arguments by the ApplyFunction operation.')

	def compute_on_args(self, *args):
		if self.python_rule is not None:
			return self.python_rule(*args)
		else:
			raise NotImplementedError



f = Function('f', 1)

g = Function('g', 1)

h = Function('h', 1)


class ApplyFunction(BinaryOperation):
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function()
		super().__init__('', 0, *children, **kwargs)

	def compute(self):
		if isinstance(self.arg, Sequence):
			args = [child.compute() for child in self.arg.children]
		else:
			args = [self.arg.compute()]
		return self.func.compute_on_args(*args)

	@property
	def func(self):
		return self.children[0]

	@property
	def arg(self):
		return self.children[1]

	@Expression.parenthesize_latex
	def __str__(self):
		if self.func.string_code is not None:
			return self.get_string_from_string_code()
		else:
			return super().__str__.__wrapped__(self)

	def get_string_from_string_code(self):
		string = ''
		for sc in self.func.string_code:
			string += self.str_from_string_code_entry(sc)
		return string

	def str_from_string_code_entry(self, entry):
		if isinstance(entry, str):
			return entry
		if isinstance(entry, Variable) and entry.symbol.startswith('child'):
			func_child_number = int(entry.symbol.split()[-1])
			return str(self.func.children[func_child_number])
		if isinstance(entry, Variable) and entry.symbol.startswith('arg'):
			if entry.symbol == 'arg':
				return str(self.arg)
			else:
				arg_child_number = int(entry.symbol.split()[-1])
				return str(self.arg.children[arg_child_number])
		if callable(entry):
			return entry(self.func)
		else:
			raise ValueError(f'Invalid glyph code entry of type {type(entry)}: {entry}')

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		count = 0
		for gc in self.func.glyph_code:
			gc = self.int_from_glyph_code_entry(gc)
			count += gc
		return count

	def get_glyphs_at_addigit(self, addigit):
		all_glyphs = set(range(0, self.glyph_count))
		arg_glyphs = set(self.get_arg_glyphs())
		if addigit == 0:
			return sorted(list(all_glyphs - arg_glyphs))
		if addigit == 1:
			return sorted(list(arg_glyphs))

	def get_arg_glyphs(self):
		start = 0
		start += self.parentheses * self.paren_length()
		for gc in self.func.glyph_code:
			if isinstance(gc, Variable) and gc.symbol == 'arg':
				end = start + self.arg.glyph_count
				return list(range(start, end))
			else:
				start += self.int_from_glyph_code_entry(gc)
		raise ValueError('arg not found in glyph_code')

	def int_from_glyph_code_entry(self, entry):
		if isinstance(entry, int):
			return entry
		if isinstance(entry, Variable) and entry.symbol.startswith('child'):
			child_number = int(entry.symbol.split()[-1])
			return self.func.children[child_number].glyph_count
		if isinstance(entry, Variable) and entry.symbol == 'arg':
			return self.arg.glyph_count
		if callable(entry):
			return entry(self.func)
		else:
			raise ValueError(f'Invalid glyph code entry of type {type(entry)}: {entry}')

	def auto_parentheses(self):
		from ..combiners.combiners import Combiner
		from ..combiners.operations import Pow
		# Usually False, true for say (f+g)(x)
		# Excepting Pow because I want to be able to write f**-1 without parentheses
		if isinstance(self.func, Combiner) and not isinstance(self.func, Pow):
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



class Composition(BinaryOperation):
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function() and children[1].is_function()
		self.eval_op = lambda x,y: Expression.__call__(x,y) # ???
		super().__init__('\\circ', 1, *children, **kwargs)






