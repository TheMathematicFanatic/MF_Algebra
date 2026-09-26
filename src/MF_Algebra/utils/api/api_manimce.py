from .api_core import MobHolderBase
from ..tex_strings import add_spaces_around_brackets
import manim
from MF_Tools import normalize_tex_svg_globally

normalize_tex_svg_globally()


# Universal to ManimCE mapping
Scene = manim.Scene
Tex = manim.MathTex #
VGroup = manim.VGroup
Write = manim.Write
Create = manim.Create #
Uncreate = manim.Uncreate
FadeIn = manim.FadeIn
FadeOut = manim.FadeOut
UP = manim.UP
DOWN = manim.DOWN
LEFT = manim.LEFT
RIGHT = manim.RIGHT
PI = manim.PI
TAU = manim.TAU


# MobHolder, will behave like a mobject
class MobHolder(MobHolderBase):
	@classmethod
	def get_mob_from_expression(cls, exp) -> manim.MathTex:
		latex = add_spaces_around_brackets(str(exp))
		tex = Tex(latex)
		return tex

	def __getitem__(self, key):
		return self.mobject[0][key]


