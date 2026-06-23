from .expression_core import Expression
from MF_Tools.dual_compatibility import dc_Tex

'''
This is a spoof Expression wrapper for what is actually just a Tex mobject.
This only exists so that Tex mobjects can go straight into a Timeline and stuff.
'''
class Texpression(Expression):
	def __init__(self, latex_string, **kwargs):
		self.latex_string = latex_string
		super().__init__(**kwargs)
	
	def init_mob(self, **kwargs):
		self._mob = dc_Tex(self.latex_string)

	def init_glyph_count(self):
		self._glyph_count = self.get_glyph_count_from_mob()

	@Expression.parenthesize_latex
	def __str__(self):
		return self.latex_string

	def compute(self):
		raise ValueError(f"Expression contains a texpression.")

	def hash_key(self):
		return (self.__class__, self.latex_string)
