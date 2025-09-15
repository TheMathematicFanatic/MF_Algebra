from ..expression_core import *
from .functions import Function
from ..numbers.integer import Integer
from ..numbers.real import e


class Log(Function):
	def __init__(self, base, allow_nickname = True, **kwargs):
		super().__init__(
			parentheses_mode = 'weak',
			**kwargs
        )
		base = Smarten(base)
		self.children.append(base)
		if base.is_identical_to(Integer(10)) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\log'
			self.symbol_glyph_length = 3
		elif base.is_identical_to(e) and allow_nickname:
			self.nicknamed = True
			self.symbol = '\\ln'
			self.symbol_glyph_length = 2
		else:
			self.nicknamed = False
			self.symbol = f'\\log_{base}'

	@property
	def base(self):
		return self.children[1]

	def get_symbol_string(self):
		if self.nicknamed:
			if self.base.is_identical_to(Integer(10)):
				return '\\log'
			elif self.base.is_identical_to(e):
				return '\\ln'
		return '\\log_{' + str(self.base) + '}'

	@Expression.parenthesize_glyph_count
	def get_glyph_count(self):
		if self.nicknamed:
			return self.symbol_glyph_length
		return self.base_glyph_count() + self.log_glyph_count() + self.arg.glyph_count

	def base_glyph_count(self):
		if self.nicknamed:
			return 0
		else:
			return self.base.glyph_count

	def log_glyph_count(self):
		if self.nicknamed and self.base.is_identical_to(e):
			return 2
		else:
			return 3

	def get_glyphs_at_addigit(self, addigit):
		start = 0
		start += self.parentheses * self.paren_length()
		if addigit == 0:
			start += self.base_glyph_count()
			start += self.log_glyph_count()
			end = start + self.arg.glyph_count
			return list(range(start, end))
		elif addigit == 1:
			start += self.log_glyph_count()
			end = start + self.base_glyph_count()
			return list(range(start, end))

	def get_func_glyphs_with_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		end = start + self.base_glyph_count()
		end += self.log_glyph_count()
		return list(range(start, end))

	def get_func_glyphs_without_extras(self):
		start = 0
		start += self.parentheses * self.paren_length()
		start += self.base_glyph_count()
		end = start + self.log_glyph_count()
		return list(range(start, end))


ln = Log(e)
