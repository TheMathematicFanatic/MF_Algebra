from ..expression_core import *
from .combiners import Combiner


class Operation:
	eval_op = None


class BinaryOperation(Combiner, Operation):
	def compute(self):
		result = self.children[0].compute()
		for child in self.children[1:]:
			result = self.eval_op(result, child.compute())
		return result

class Add(BinaryOperation):
	symbol = '+'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x, y: x + y)

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()
		return self

	def is_negative(self):
		return self.children[0].is_negative()

class Sub(BinaryOperation):
	symbol = '-'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x, y: x - y)

	def auto_parentheses(self):
		for i, child in enumerate(self.children):
			if i > 0 and (isinstance(child, (Add, Sub)) or child.is_negative()):
				child.give_parentheses()
			child.auto_parentheses()
		return self

	def is_negative(self):
		return self.children[0].is_negative()

class Mul(BinaryOperation):
	mode = 'config'
	eval_op = staticmethod(lambda x, y: x * y)
	
	def auto_determine_mode(self):
		from ..numbers.number import Number
		if all(isinstance(child, Number) for child in list(map(Smarten, self.children))):
			return 'dot'
		else:
			return 'juxtapose'

	@property
	def symbol(self):
		mode = self.mode
		if mode == 'config':
			mode = algebra_config['multiplication_mode']
		if mode == 'auto':
			mode = self.auto_determine_mode()
		symbol_dict = {
			'dot': '\\cdot',
			'x': '\\times',
			'juxtapose': ''
		}
		if mode in symbol_dict:
			return symbol_dict[mode]
		else:
			raise ValueError(f"Invalid multiplication mode: {mode}. Mode must be among {list(symbol_dict.keys())}")

	@property
	def symbol_glyph_length(self):
		mode = self.mode
		if mode == 'auto':
			mode = self.auto_determine_mode()
		glyph_length_dict = {
			'dot': 1,
			'x': 1,
			'juxtapose': 0
		}
		if mode in glyph_length_dict:
			return glyph_length_dict[mode]
		else:
			raise ValueError(f"Invalid multiplication mode: {mode}. Mode must be among {list(glyph_length_dict.keys())}")

	def auto_parentheses(self): # should be more intelligent based on mode
		for child in self.children:
			if isinstance(child, (Add, Sub)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()
		return self

	def is_negative(self):
		return self.children[0].is_negative()

class Div(BinaryOperation):
	eval_op = staticmethod(lambda x, y: x / y)
	mode = 'fraction'

	@property
	def symbol(self):
		mode = self.mode
		symbol_dict = {
			'fraction': '\\over',
			'inline': '\\div',
		}
		if mode in symbol_dict:
			return symbol_dict[mode]
		else:
			raise ValueError(f"Invalid division mode: {mode}. Mode must be among {list(symbol_dict.keys())}")

	@property
	def symbol_glyph_length(self):
		mode = self.mode
		glyph_length_dict = {
			'fraction': 1,
			'inline': 1,
		}
		if mode in glyph_length_dict:
			return glyph_length_dict[mode]
		else:
			raise ValueError(f"Invalid division mode: {mode}. Mode must be among {list(glyph_length_dict.keys())}")

	def auto_parentheses(self):
		for child in self.children:
			if (isinstance(child, (Add, Sub, Mul, Div)) or child.is_negative()) and algebra_config["division_mode"] == "inline":
				child.give_parentheses()
			child.auto_parentheses()
		return self

	def is_negative(self):
		return self.children[0].is_negative() or self.children[1].is_negative()
	
	def compute(self):
		num = self.children[0].compute()
		den = self.children[1].compute()
		if den == 0:
			raise ZeroDivisionError
		if num % den == 0:
			return int(num / den)
		else:
			return float(num) / float(den)

class Pow(BinaryOperation):
	symbol = '^'
	symbol_glyph_length = 0
	eval_op = staticmethod(lambda x, y: x ** y)

	def auto_parentheses(self):
		assert len(self.children) == 2, f'Children: {self.children}' #idc how to auto paren power towers
		if isinstance(self.children[0], BinaryOperation) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		for child in self.children:
			child.auto_parentheses()
		return self

	def is_negative(self):
		return False


class UnaryOperation(Expression, Operation):
	symbol = None
	symbol_glyph_length = None
	eval_op = None

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return self.symbol_glyph_length + self.children[0].glyph_count

	@Expression.parenthesize_latex
	def __str__(self):
		return self.symbol + str(self.children[0])
	
	def compute(self):
		return self.eval_op(self.children[0].compute())

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'-': 'get_unary_glyph',
		'~': 'get_unary_glyph'
	}

	def get_unary_glyph(self):
		return list(range(0, self.symbol_glyph_length))
	
	def get_glyphs_at_addigit(self, addigit):
		if addigit == 0:
			start = 0
			start += self.parentheses * self.paren_length()
			start += self.symbol_glyph_length
			end = start + self.children[0].glyph_count
			return list(range(start, end))
		else:
			raise NotImplementedError(f"{self} has no children at index {addigit}")

class Negative(UnaryOperation):
	symbol = '-'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x: -x)

	def auto_parentheses(self):
		if isinstance(self.children[0], (Add, Sub)) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		self.children[0].auto_parentheses()
		return self

	def is_negative(self):
		return True
