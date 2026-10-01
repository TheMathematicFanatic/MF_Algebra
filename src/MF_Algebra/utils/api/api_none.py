from .api_core import MobHolderBase
import numpy as np


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


# Universal to blank objects mapping
Scene = blank_class()
Tex = blank_class()
VGroup = blank_class()
Write = blank_class()
Create = blank_class()
Uncreate = blank_class()
FadeIn = blank_class()
FadeOut = blank_class()
UP = np.array([0, 1, 0])
DOWN = np.array([0, -1, 0])
LEFT = np.array([-1, 0, 0])
RIGHT = np.array([1, 0, 0])
PI = np.pi
TAU = 2*np.pi
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








