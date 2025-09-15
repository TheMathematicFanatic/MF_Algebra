from ..expression_core import *
from .functions import Function
from ..numbers.integer import Integer


class Rad(Function):
	def __init__(self, index, allow_nickname = True, **kwargs):
		super().__init__(
			parentheses_mode = 'never',
			**kwargs
        )
		index = Smarten(index)
		self.children.append(index)
		if index.is_identical_to(Integer(2)) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\sqrt'
		else:
			self.nicknamed = False
			self.symbol = f'\\sqrt[{index}]'
	
	@property
	def index(self):
		return self.children[1]

	def get_symbol_string(self):
		if self.nicknamed:
			return '\\sqrt'
		return f'\\sqrt[{self.index}]'

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		return self.index_glyph_count() + self.radical_glyph_count() + self.arg.glyph_count

	def index_glyph_count(self):
		if self.nicknamed:
			return 0
		else:
			return self.index.glyph_count

	def radical_glyph_count(self):
		if algebra_config['fast_root_length']:
			return 2
		else:
			raise NotImplementedError

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		if addigit == 0:
			start += self.index_glyph_count()
			start += self.radical_glyph_count()
			end = start + self.children[0].glyph_count
			return list(range(start, end))
		elif addigit == 1:
			end = start + self.index_glyph_count()
			return list(range(start, end))

	def get_func_glyphs_with_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		end = start + self.index_glyph_count()
		end += self.radical_glyph_count()
		return list(range(start, end))

	def get_func_glyphs_without_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		start += self.index_glyph_count()
		end = start + self.radical_glyph_count()
		return list(range(start, end))


sqrt = Rad(2)

cbrt = Rad(3)
