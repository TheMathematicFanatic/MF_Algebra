from ..expression_core import *
from .combiners import *


class Relation(Combiner):
	def compute(self):
		return all([self.eval_op(self.children[i].compute(), self.children[i+1].compute()) for i in range(len(self.children)-1)])


class Equation(Relation):
	symbol = '='
	symbol_glyph_length = 1
	eval_op = lambda x, y: x == y

class LessThan(Relation):
	symbol = '<'
	symbol_glyph_length = 1
	eval_op = lambda x, y: x < y

class GreaterThan(Relation):
	symbol = '>'
	symbol_glyph_length = 1
	eval_op = lambda x, y: x > y

class LessThanOrEqualTo(Relation):
	symbol = '\\leq'
	symbol_glyph_length = 1
	eval_op = lambda x, y: x <= y

class GreaterThanOrEqualTo(Relation):
	symbol = '\\geq'
	symbol_glyph_length = 1
	eval_op = lambda x, y: x >= y
