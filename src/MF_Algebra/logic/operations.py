from ..expressions.combiners.operations import UnaryOperation, BinaryOperation
from .booleans import BooleanExpression


class BooleanOperation(BooleanExpression):
	def auto_parentheses(self):
		for child in self.children:
			if isinstance(child, BinaryOperation):
				child.give_parentheses()
			child.auto_parentheses()
		return self


class Not(BooleanOperation, UnaryOperation):
	symbol = '\\neg'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P: not P)


class And(BooleanOperation, BinaryOperation):
	symbol = '\\land'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P and Q)


class Or(BooleanOperation, BinaryOperation):
	symbol = '\\lor'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P or Q)


class Xor(BooleanOperation, BinaryOperation):
	symbol = '\\oplus'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P != Q)


class Implies(BooleanOperation, BinaryOperation):
	symbol = '\\Rightarrow'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: not P or Q)


class Iff(BooleanOperation, BinaryOperation):
	symbol = '\\Leftrightarrow'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P == Q)

