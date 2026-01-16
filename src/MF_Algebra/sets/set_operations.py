from .set_core import Set
from ..expressions import BinaryOperation, Relation, Pow


class SetRelation(Relation):
	pass


class IsElement(SetRelation):
	symbol = '\\in'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda a, A: a in A)


class IsSubset(SetRelation):
	symbol = '\\subseteq'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda A, B: all(a in B for a in A))


class IsProperSubset(SetRelation):
	symbol = '\\subset'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda A, B: all(a in B for a in A) and any(b in A for b in B))



class SetOperation(Set, BinaryOperation):
	in_op = staticmethod(lambda A, a: a in A)

	def contains(self, item):
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


class CartesianProduct(SetOperation):
	symbol = '\\times'
	symbol_glyph_length = 1
	in_rule = lambda A, a: all(ai in Ai for ai,Ai in zip(a.children,A.children))

	def get_tuple_set(self):
		from .set_core import ElementsSet
		from itertools import product
		return ElementsSet(*product(*self.children))


class CartesianPower(Pow, Set):
	in_rule = lambda An, a: len(a.children) == An.power and all(ai in An.base for ai in a.children)

	@property
	def power(self):
		return self.children[1].compute()

	@property
	def base(self):
		return self.children[0]

	def get_cartesian_product(self):
		return CartesianProduct(*[self.base.copy() for _ in range(self.power)])

	def get_tuple_set(self):
		return self.get_cartesian_product().get_tuple_set()




