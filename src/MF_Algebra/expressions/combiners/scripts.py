from .combiners import Combiner, CombinerContainer


class Script(Combiner):
	def auto_parentheses(self):
		from .operations import Operation
		for i,child in enumerate(self.children):
			if i==0 and isinstance(child, (Combiner, Operation)):
				child.give_parentheses()
			child.auto_parentheses()
		return self

	def is_variable(self):
		from ..variables import Variable
		return isinstance(self.children[0], Variable)

class Subscript(Script):
	symbol = '_'
	symbol_glyph_length = 0

class Superscript(Script):
	symbol = '^'
	symbol_glyph_length = 0

class Subscripts_R(CombinerContainer):
	expression_type = Subscript
	shared_side = 'right'

class Subscripts_L(CombinerContainer):
	expression_type = Subscript
	shared_side = 'left'

class Superscripts_R(CombinerContainer):
	expression_type = Superscript
	shared_side = 'right'

class Superscripts_L(CombinerContainer):
	expression_type = Superscript
	shared_side = 'left'


from ..variables import x,y,z
x1,x2,x3 = Subscripts_L(x,1,2,3)
y1,y2,y3 = Subscripts_L(y,1,2,3)
z1,z2,z3 = Subscripts_L(z,1,2,3)

