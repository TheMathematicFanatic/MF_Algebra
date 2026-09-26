from .api_core import MobHolderBase
from ..tex_strings import add_spaces_around_brackets
import manimlib
from MF_Tools import normalize_tex_svg_globally

normalize_tex_svg_globally()


# Universal to ManimGL mapping
Scene = manimlib.Scene
Tex = manimlib.Tex #
VGroup = manimlib.VGroup
Write = manimlib.Write
Create = manimlib.ShowCreation #
Uncreate = manimlib.Uncreate
FadeIn = manimlib.FadeIn
FadeOut = manimlib.FadeOut
UP = manimlib.UP
DOWN = manimlib.DOWN
LEFT = manimlib.LEFT
RIGHT = manimlib.RIGHT
PI = manimlib.PI
TAU = manimlib.TAU


# MobHolder, will behave like a mobject
class MobHolder(MobHolderBase):
	@classmethod
	def get_mob_from_expression(cls, exp) -> manimlib.Tex:
		latex = add_spaces_around_brackets(str(exp))
		tex = Tex(latex)
		return tex

	def __getitem__(self, key):
		return self.mobject[key]








