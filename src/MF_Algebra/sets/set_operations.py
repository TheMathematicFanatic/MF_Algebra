from .set_core import Set
from ..expressions.combiners.operations import BinaryOperation
from ..expressions.combiners.relations import Relation


class In(Relation):
	symbol = '\\in'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda a, A: a in A)




class SetOperation(BinaryOperation):
	in_op = staticmethod(lambda A, a: a in A)

	def __contains__(self, item):
		return self.in_op(item)


class Intersection(SetOperation):
	symbol = '\\cap'
	symbol_glyph_length = 1
	in_op = staticmethod(lambda A, a: all(a in Ai for Ai in A.children))


class Union(SetOperation):
	symbol = '\\cup'
	symbol_glyph_length = 1
	in_op = staticmethod(lambda A, a: any(a in Ai for Ai in A.children))


class Difference(SetOperation):
	symbol = '\\setminus'
	symbol_glyph_length = 1
	in_op = staticmethod(lambda A, a: a in A.children[0] and not any(a in Ai for Ai in A.children[1:]))


