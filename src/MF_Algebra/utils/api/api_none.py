from .api_core import MobHolderBase



# Universal to blank objects mapping
Scene = type
Tex = type
VGroup = type
Write = type
Create = type
Uncreate = type
FadeIn = type
FadeOut = type
UP = [0, 1, 0]
DOWN = [0, -1, 0]
LEFT = [-1, 0, 0]
RIGHT = [1, 0, 0]
PI = 3.14159265358979
TAU = 2*PI



# MobHolder, will behave like a mobject
class MobHolder(MobHolderBase):
	@classmethod
	def get_mob_from_expression(cls, exp) -> str:
		latex = str(exp)
		return latex

	def __getitem__(self, key):
		return None
	
	def __getattr__(self, name):
		return None
	
	








