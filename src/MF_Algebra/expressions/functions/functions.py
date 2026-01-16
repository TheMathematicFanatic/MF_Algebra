from ..expression_core import *
from ..combiners.sequences import Sequence
from ..combiners.operations import BinaryOperation
from ..variables import Variable


arg = Variable('arg')
arg_num = lambda n: Variable(f'arg {n}')
arg0 = arg_num(0)
arg1 = arg_num(1)
arg2 = arg_num(2)

child_num = lambda n: Variable(f'child {n}')
child = child_num(0)
c0 = child_num(0)
c1 = child_num(1)
c2 = child_num(2)


# Example glyph and string codes

# Sigma
string_code = ['\\sum_', c0, '^', c1, arg]
glyph_code = [c1, 1, c0, arg]

# Nth Root
string_code = ['\\sqrt[', c0, ']', arg]
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
		algebra_rule_variables = None,
		algebra_rule = None,
		parentheses_mode = 'always',
		children = [],
		**kwargs
	):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self._python_rule = python_rule #callable
		self.algebra_rule = algebra_rule
		if algebra_rule_variables is not None:
			self.algebra_rule_variables = algebra_rule_variables
		elif algebra_rule is not None:
			self.algebra_rule_variables = algebra_rule.get_all_variables()
		self.parentheses_mode = parentheses_mode
		super().__init__(*children, **kwargs)

	@property
	def python_rule(self):
		if self._python_rule:
			return self._python_rule
		else:
			raise NotImplementedError

	@Expression.parenthesize_latex
	def __str__(self):
		return self.get_string_from_code()

	def get_string_from_code(self):
		string = ''
		for sc in self.string_code:
			string += get_value_from_code_entry(self, sc, str)
		return string

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		count = 0
		for gc in self.glyph_code:
			count += get_value_from_code_entry(self, gc, int)
		return count

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		for gc in self.glyph_code:
			if isinstance(gc, Variable) and gc == child_num(addigit):
				end = start + self.children[addigit].glyph_count
				return list(range(start, end))
			else:
				start += get_value_from_code_entry(self, gc, int)
		return []

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'f': 'get_main_func_glyphs',
		'F': 'get_all_func_glyphs',
		'c': 'get_all_child_glyphs',
	}

	def get_all_child_glyphs(self):
		glyphs = []
		for addigit in range(len(self.children)):
			glyphs += self.get_glyphs_at_addigit(addigit)
		return sorted(glyphs)

	def get_main_func_glyphs(self):
		return sorted(list(set(self.get_all_func_glyphs()) - set(self.get_all_child_glyphs())))

	def get_all_func_glyphs(self): # Needs glyph_code rework...
		# The trouble is we need the glyph counts for the argument(s) in case there are after them like n!
		return list(range(0, self.glyph_count))

	def is_function(self):
		return True

	def compute(self):
		raise ValueError('Functions should not be computed directly. It can be computed on its arguments by the ApplyFunction operation.')

	def compute_on_args(self, *computed_args):
		if self.python_rule is not None:
			return self.python_rule(*computed_args)
		elif self.algebra_rule and self.algebra_rule_variables:
			def rule(*args):
				assert len(args) == len(self.algebra_rule_variables), 'Mismatched number of arguments'
				substitution = {var: arg for var, arg in zip(self.algebra_rule_variables, args)}
				result = self.algebra_rule @ substitution
				return result.compute()
			self.python_rule = rule
			return rule(*computed_args)
		else:
			raise NotImplementedError('No python_rule or algebra_rule defined for this function')

	def expand_on_args(self, *arg_expressions):
		if self.algebra_rule is not None:
			assert len(self.algebra_rule_variables) == len(arg_expressions), 'Mismatched number of arguments'
			return self.algebra_rule @ {var: arg for var, arg in zip(self.algebra_rule_variables, arg_expressions)}
		else:
			raise NotImplementedError

	def evaluate(self, *arg_expressions):
		# Override for special values like trig
		computed_args = [arg.compute() for arg in arg_expressions]
		computed_value = self.compute_on_args(*computed_args)
		return Smarten(computed_value)

	def hash_key(self):
		return (self.__class__, tuple(self.children), self.symbol)

	@property
	def equation(self, **kwargs):
		from ..combiners.relations import Equation
		return Equation(self(*self.algebra_rule_variables), self.algebra_rule)

	@property
	def lambdify(self):
		assert self.algebra_rule is not None, 'This function has no algebra rule'
		from ...utils import to_sympy
		from sympy import lambdify
		sympy_vars = [to_sympy(v) for v in self.algebra_rule_variables]
		sympy_rule = to_sympy(self.algebra_rule)
		return lambdify(sympy_vars, sympy_rule, 'math')



class ApplyFunction(BinaryOperation):
	symbol = ''
	symbol_glyph_length = 0
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function()
		super().__init__(*children, **kwargs)

	def compute(self):
		computed_args = [arg.compute() for arg in self.args_list]
		return self.func.compute_on_args(*computed_args)

	@property
	def func(self):
		return self.children[0]

	@property
	def arg(self):
		return self.children[1]

	@property
	def args_list(self):
		if isinstance(self.arg, Sequence):
			return [*self.arg.children]
		else:
			return [self.arg]

	@Expression.parenthesize_latex
	def __str__(self):
		if hasattr(self.func, 'string_code'):
			return self.get_string_from_string_code()
		else:
			return super().__str__.__wrapped__(self)

	def get_string_from_string_code(self):
		string = ''
		for sc in self.func.string_code:
			string += get_value_from_code_entry(self, sc, str)
		return string

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		count = 0
		for gc in self.func.glyph_code:
			count += get_value_from_code_entry(self, gc, int)
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
				start += get_value_from_code_entry(self, gc, int)
		raise ValueError('arg not found in glyph_code')

	def auto_parentheses(self):
		from ..combiners.sequences import Sequence
		from ..combiners.operations import Add, Sub, Mul
		# Usually False, true for say (f+g)(x)
		if isinstance(self.func, (Sequence, Add, Sub, Mul, Composition)):
			self.func.give_parentheses(True)
		self.func.auto_parentheses()

		parentheses_mode = getattr(self.func, 'parentheses_mode', 'always')
		if parentheses_mode == 'always':
			self.arg.give_parentheses(True)
		from ..combiners.operations import Operation
		if parentheses_mode == 'strong' and (isinstance(self.arg, Operation) or self.arg.is_negative()):
			self.arg.give_parentheses(True)
		from ..combiners.operations import Add, Sub
		if parentheses_mode == 'weak' and (isinstance(self.arg, (Add, Sub)) or self.arg.is_negative()):
			self.arg.give_parentheses(True)
		if parentheses_mode == 'var only' and not self.arg.is_variable():
			self.arg.give_parentheses(True)
		if parentheses_mode == 'never':
			self.arg.give_parentheses(False)
		self.arg.auto_parentheses()

		return self

	def is_function(self):
		# This should always be False because it can no longer be called on something
		# Maybe not in very bold circumstances, but this will do for now
		return False

	def expand_on_args(self):
		return self.func.expand_on_args(*self.args_list)

	def evaluate(self):
		try:
			result = self.expand_on_args()
		except NotImplementedError:
			result = self.func.evaluate(*self.args_list)
		return result

	def equation_from_args(self, **kwargs):
		from ..combiners.relations import Equation
		return Equation(self, self.expand_on_args(**kwargs))


class Composition(BinaryOperation):
	symbol = '\\circ'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x,y: Expression.__call__(x,y)) # ???
	string_code = [c0, lambda self: self.symbol, c1]
	glyph_code = [c0, lambda self: self.symbol_glyph_length, c1]
	def __init__(self, *children, **kwargs):
		assert len(children) == 2
		assert children[0].is_function() and children[1].is_function()
		super().__init__(*children, **kwargs)


def get_value_from_code_entry(expression, entry, desired_type):
	if isinstance(entry, desired_type):
		return entry

	if isinstance(expression, Function):
		func = expression
	elif isinstance(expression, ApplyFunction):
		func = expression.func
		arg = expression.arg
	else:
		raise ValueError('Function or ApplyFunction expected')

	if isinstance(entry, Variable):
		if entry.symbol.startswith('child'):
			func_child_number = int(entry.symbol.split()[-1])
			target = func.children[func_child_number]
		elif entry.symbol.startswith('arg'):
			if isinstance(expression, Function):
				return desired_type()
			if entry.symbol == 'arg':
				target = arg
			else:
				arg_child_number = int(entry.symbol.split()[-1])
				target = func.children[arg_child_number]
		else:
			raise ValueError('Invalid code variable: ' + entry.symbol)
		if desired_type == int:
			return target.glyph_count
		elif desired_type == str:
			return '{' + str(target) + '}'
		else:
			raise ValueError('Invalid desired_type. Must be int or str')

	if callable(entry):
		return desired_type(entry(func))

	raise ValueError(f'Invalid glyph code entry of type {type(entry)}: {entry}')



f = Function('f', 1)
g = Function('g', 1)
h = Function('h', 1)


from ..expression_core import ExpressionContainer
class Functions(ExpressionContainer):
	expression_type = Function
