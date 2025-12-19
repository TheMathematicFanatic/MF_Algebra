from .combiners import Combiner


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


from ..variables import x,y,z

x1 = Subscript(x,1)
x2 = Subscript(x,2)
x3 = Subscript(x,3)
y1 = Subscript(y,1)
y2 = Subscript(y,2)
y3 = Subscript(y,3)
z1 = Subscript(z,1)
z2 = Subscript(z,2)
z3 = Subscript(z,3)
