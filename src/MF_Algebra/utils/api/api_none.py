from .api_core import MobHolderBase
import math


def blank_class():
	class blank:
		def __init__(self, label=None, *args, **kwargs):
			self.label = label
		
		def __repr__(self):
			return self.label
		
		def __str__(self):
			return self.label

		def __getattr__(self, name):
			return None
	return blank


class numpy_like_array(list):
	def __mul__(self, other):
		return numpy_like_array([element*other for element in self])


# Universal to blank objects mapping
Scene = blank_class()
Tex = blank_class()
VGroup = blank_class()
Write = blank_class()
Create = blank_class()
Uncreate = blank_class()
FadeIn = blank_class()
FadeOut = blank_class()
UP = numpy_like_array([0, 1, 0])
DOWN = numpy_like_array([0, -1, 0])
LEFT = numpy_like_array([-1, 0, 0])
RIGHT = numpy_like_array([1, 0, 0])
PI = math.pi
TAU = 2*math.pi
TransformByGlyphMap = blank_class()
TransformMatchingTex = blank_class()
AnimationGroup = blank_class()



# MobHolder, will behave like a mobject
class MobHolder(MobHolderBase):
	@classmethod
	def get_mob_from_expression(cls, exp) -> str:
		latex = str(exp)
		return latex

	def __getitem__(self, key):
		return None
	
	def __getattr__(self, name):
		if name.startswith('__'):
			raise AttributeError
		else:
			return lambda *a, **k: None

	def set_color(self, *args, **kwargs):
		return None








