from ..expressions.combiners.operations import UnaryOperation, BinaryOperation


class Not(UnaryOperation):
	symbol = '\\neg'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P: not P)
	def auto_parentheses(self):
		if isinstance(self.children[0], BinaryOperation):
			self.children[0].give_parentheses()
		self.children[0].auto_parentheses()
		return self


class And(BinaryOperation):
	symbol = '\\land'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P and Q)


class Or(BinaryOperation):
	symbol = '\\lor'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P or Q)


class Xor(BinaryOperation):
	symbol = '\\oplus'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P != Q)


class Implies(BinaryOperation):
	symbol = '\\land'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: not P or Q)


class Iff(BinaryOperation):
	symbol = '\\land'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda P, Q: P == Q)

