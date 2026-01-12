from ..expressions import Expression, Sequence, Variable


class Set(Expression):
	in_rule = None
	def __init__(self,
		*children,
		in_rule = None, # condition to check if input is in set
		**kwargs
	):
		super().__init__(*children, **kwargs)
		self.in_rule = in_rule or self.in_rule

	def __contains__(self, item):
		if self.in_rule:
			return self.in_rule(item)

	def __and__(self, other):
		from .set_operations import Intersection
		return Intersection(self, other)

	def __or__(self, other):
		from .set_operations import Union
		return Union(self, other)

	def __sub__(self, other):
		from .set_operations import Difference
		return Difference(self, other)

	def __truediv__(self, other):
		from .set_operations import Difference
		return Difference(self, other)



class ElementsSet(Set, Sequence):
	def __init__(self,
		*children,
		in_rule = None, #condition to check if input is in set
		**kwargs
	):
		super().__init__(*children, **kwargs)
		self._set = set(children)
		self.in_rule = in_rule or self.in_rule
		self.give_parentheses(True, symbols = ('{','}'))

	def __contains__(self, item):
		return item in self._set

	def __iter__(self):
		return iter(self._set)


class SymbolSet(Set, Variable):
	symbol = None
	in_rule = None

















Empty = SymbolSet(symbol='\\varnothing', symbol_glyph_length=1, in_rule=lambda x: False)
Empty.elements = ElementsSet()


from ..utils import Smarten
from ..expressions.numbers import Integer, Real
from ..expressions.variables import dots

Z = SymbolSet(symbol='\\mathbb{Z}', symbol_glyph_length=1, in_rule=lambda x: isinstance(Smarten(x), Integer))
Z.elements = ElementsSet(dots, -3, -2, -1, 0, 1, 2, 3, dots)

N = SymbolSet(symbol='\\mathbb{N}', symbol_glyph_length=1, in_rule=lambda x: isinstance(Smarten(x), Integer) and x.value >= 0)
N.elements = ElementsSet(0, 1, 2, 3, dots)

R = SymbolSet(symbol='\\mathbb{R}', symbol_glyph_length=1, in_rule=lambda x: isinstance(Smarten(x), Real))




