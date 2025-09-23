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
		return joiner.join(["{" + str(child) + "}" for child in self.children])

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

	def get_glyphs_at_addigit(self, addigit:int):
		start = 0
		start += self.parentheses * self.paren_length()
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
		# This is horrible we gotta find another way lol
		self.children[0].is_variable = lambda *args: False
		return isinstance(self, Variable) or isinstance(self.children[0], Variable)

class Subscript(Script):
	symbol = '_'
	symbol_glyph_length = 0

class Superscript(Script):
	symbol = '^'
	symbol_glyph_length = 0
