from ..expressions import Expression


class Set(Expression):
	in_rule = None
	_set = set()

	def __init__(self,
		*children,
		in_rule = None, # condition to check if input is in set
		**kwargs
	):
		super().__init__(*children, **kwargs)
		self.in_rule = self.in_rule or in_rule

	def __contains__(self, item):
		# x in A (must return bool)
		if self.in_rule:
			return self.in_rule(Smarten(item))
		else:
			return item in self._set

	def __iter__(self):
		return iter(self._set)

	def __and__(self, other):
		from .set_operations import Intersection
		return Intersection(self, other)

	def __rand__(self, other):
		from .set_operations import Intersection
		return Intersection(other, self)

	def __or__(self, other):
		from .set_operations import Union
		return Union(self, other)
	
	def __ror__(self, other):
		from .set_operations import Union
		return Union(other, self)

	def __sub__(self, other):
		from .set_operations import Difference
		return Difference(self, other)
	
	def __rsub__(self, other):
		from .set_operations import Difference
		return Difference(other, self)

	def __truediv__(self, other):
		from .set_operations import Difference
		return Difference(self, other)
	
	def __rtruediv__(self, other):
		from .set_operations import Difference
		return Difference(other, self)
	
	def __rmod__(self, other):
		from .set_operations import IsElement
		return IsElement(other, self)
	
	def __lt__(self, other):
		from .set_operations import IsProperSubset
		return IsProperSubset(self, other)
	
	def __le__(self, other):
		from .set_operations import IsSubset
		return IsSubset(self, other)
	
	def __mul__(self, other):
		from .set_operations import CartesianProduct
		return CartesianProduct(self, other)
	
	def __rmul__(self, other):
		from .set_operations import CartesianProduct
		return CartesianProduct(other, self)

	def __pow__(self, other):
		from .set_operations import CartesianPower
		return CartesianPower(self, other)
	
	def __rpow__(self, other):
		from .set_operations import CartesianPower
		return CartesianPower(other, self)



from ..expressions import Sequence
class ElementsSet(Set, Sequence):
	parentheses = True
	paren_symbols = ('\\{','\\}')

	def __init__(self,
		*children,
		in_rule = None, #condition to check if input is in set
		**kwargs
	):
		super().__init__(*children, **kwargs)
		self._set = set(children)
		self.in_rule = in_rule or self.in_rule


from ..expressions import Variable
class SymbolSet(Set, Variable):
	symbol = None
	in_rule = None


from ..expressions import ExpressionContainer
class Sets(ExpressionContainer):
	expression_type = SymbolSet


from ..expressions import Combiner
class SetBuilder(Set, Combiner):
	symbol = '|'
	symbol_glyph_length = 1
	left_spacing = '\\enspace'
	right_spacing = '\\enspace'
	parentheses = True
	paren_symbols = ('\\{','\\}')

	def __init__(self, expr, *conditions, **kwargs):
		super().__init__(expr, Sequence(*conditions), **kwargs)
	










from ..expressions import Integer, Real, dots
from ..utils import Smarten

Empty = SymbolSet(symbol='\\varnothing', symbol_glyph_length=1, in_rule=lambda x: False)
Empty.elements = ElementsSet()

Z = SymbolSet(
	symbol = '\\mathbb{Z}',
	symbol_glyph_length = 1,
	in_rule = lambda x: isinstance(Smarten(x).compute(), Integer)
	)
Z.elements = ElementsSet(dots, -2, -1, 0, 1, 2, dots)

N = SymbolSet(
	symbol = '\\mathbb{N}',
	symbol_glyph_length = 1,
	in_rule = lambda x: isinstance(Smarten(x).compute(), Integer) and x.value >= 0
)
N.elements = ElementsSet(0, 1, 2, 3, dots)

R = SymbolSet(
	symbol = '\\mathbb{R}', 
	symbol_glyph_length = 1,
	in_rule = lambda x: isinstance(Smarten(x).compute(), (Integer, Real))
)




