from ..expression_core import *


class Combiner(Expression):
	symbol = None
	symbol_glyph_length = None
	left_spacing = ''
	right_spacing = ''

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		count = sum([child.glyph_count for child in self.children])
		count += self.symbol_glyph_length * (len(self.children) - 1)
		return count

	@Expression.parenthesize_latex
	def __str__(self, *args, **kwargs):
		joiner = self.left_spacing + self.symbol + self.right_spacing
		return joiner.join([str(child) for child in self.children])

	def set_spacing(self, left_spacing, right_spacing):
		self.left_spacing = left_spacing
		self.right_spacing = right_spacing

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'+': 'get_op_glyphs',
		'-': 'get_op_glyphs',
		'*': 'get_op_glyphs',
		'/': 'get_op_glyphs',
		'^': 'get_op_glyphs',
		'=': 'get_op_glyphs',
		'<': 'get_op_glyphs',
		'>': 'get_op_glyphs',
		',': 'get_op_glyphs',
	}

	@Expression.parenthesize_glyph_list
	def get_glyphs_at_addigit(self, addigit:int):
		start = 0
		for sibling in self.children[:addigit]:
			start += sibling.glyph_count
			start += self.symbol_glyph_length
		child = self.children[addigit]
		end = start + child.glyph_count
		return list(range(start, end))

	def get_op_glyphs(self):
		results = []
		turtle = self.parentheses * self.paren_length()
		for child in self.children[:-1]:
			turtle += child.glyph_count
			results += list(range(turtle, turtle + self.symbol_glyph_length))
			turtle += self.symbol_glyph_length
		return results



class CombinerContainer(ExpressionContainer):
	# Good for making subscripts for example
	expression_type = Combiner
	shared_side = 'left'
	def generate_elements(self, *strings):
		if self.shared_side == 'left': # x1,x2,x3 = Subscripts(x,1,2,3)
			older_sibling = strings[0]
			younger_siblings = strings[1:]
			return [self.expression_type(older_sibling, younger) for younger in younger_siblings]
		elif self.shared_side == 'right': # xi,yi = Subscripts(x,y,i,)
			older_sibling = strings[-1]
			younger_siblings = strings[:-1]
			return [self.expression_type(younger, older_sibling) for younger in younger_siblings]
