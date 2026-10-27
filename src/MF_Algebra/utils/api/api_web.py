import js
from jsffi import to_js
from .api_core import MobHolderBase
import sys
from types import ModuleType
import asyncio



def js_obj(d:dict):
	return to_js(d, dict_converter=js.Object.fromEntries)


class Glyph:
	def __init__(self, element, character=None):
		self.element = element
		self.character = character

	def set_color(self, color):
		self.element.style.fill = color
		self.element.style.stroke = color
		return self

	def __repr__(self):
		return f'Glyph({self.character})'



class VGroup:
	def __init__(self, *items):
		self.items = list(items)
	
	def set_color(self, color):
		for item in self:
			item.set_color(color)
		return self
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			return VGroup(*self.items[key])
		return self.items[key]
	
	def __iter__(self):
		return iter(self.items)
	
	def __len__(self):
		return len(self.items)
	
	def add(self, *items):
		self.items += list(items)
		return self

	def shift(self, vector): pass
	def move_to(self, vector): pass
	def scale(self, scalar): pass




class Tex(VGroup):
	def __init__(self, latex, display=True):
		self.container = js.MathJax.tex2svg(latex, js_obj({"display": display}))
		svg = self.container.querySelector("svg")
		flattened = js.mathjaxFlatten(svg)
		for warning in flattened.warnings:
			print(f"Warning - Glyph at {warning.at}: {warning.why}")
		glyphs = [Glyph(s.el, s.ch) for s in flattened]
		super().__init__(*glyphs)
		self.glyphs = self.items
	




# MobHolder, will behave like a mobject
class MobHolder(MobHolderBase):
	@classmethod
	def get_mob_from_expression(cls, exp) -> Tex:
		latex = str(exp)
		tex = Tex(latex)
		return tex

	def __getitem__(self, key):
		return self.mobject[key]



class Scene:
	def __init__(self, dom_element=None):
		self.dom_element = dom_element
		self.mobjects = []
		self.play_queue = []
	
	def add(self, *mobjects):
		for mob in mobjects:
			if not mob in self.mobjects:
				self.mobjects.append(mob)
		return self

	def remove(self, *mobjects):
		for mob in mobjects:
			if mob in self.mobjects:
				self.mobjects.remove(mob)
		return self

	def clear(self):
		self.mobjects = []
		return self

	def wait(self, time):
		pass

	def play(self, *animations, run_time=1, **kwargs):
		pass







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



Animation = blank_class()

class AnimationGroup(Animation): pass

class FadeIn(Animation): pass

class FadeOut(Animation): pass

class Write(Animation): pass

class Create(Animation): pass

class Uncreate(Animation): pass

class TransformByGlyphMap(Animation): pass

class TransformMatchingTex(Animation): pass





class ModuleWrapper:
	original_module = None
	def __getattr__(self, name):
		try:
			if isinstance(self.original_module, ModuleType):
				return getattr(self.original_module, name)
			else:
				return None
		except (AttributeError, ImportError):
			raise AttributeError(
				f'The {str(self.original_module)} module has replaced with a stub because it is not fully available in this environment, and it has no attribute {name}.'
				)


def _two_item_gcd(a,b):
	while b:
		a,b = b, a%b
	return abs(a)

def _two_item_lcm(a,b):
	return abs(a*b) // _two_item_gcd(a,b) if a and b else 0

import math as _original_math
class _math(ModuleWrapper):
	original_module = _original_math

	@staticmethod
	def gcd(*values):
		gcd = values[0]
		for i in range(1,len(values)):
			gcd = _two_item_gcd(gcd, values[i])
		return gcd

	@staticmethod
	def lcm(*values):
		lcm = values[0]
		for i in range(1,len(values)):
			lcm = _two_item_lcm(lcm, values[i])
		return lcm

sys.modules['math'] = _math()



class _asteval(ModuleWrapper):
	original_module = 'asteval'
sys.modules['asteval'] = _asteval()

class _tabulate(ModuleWrapper):
	original_module = 'tabulate'
sys.modules['tabulate'] = _tabulate()

class _typing(ModuleWrapper):
	original_module = 'typing'
sys.modules['typing'] = _typing()




class numpy_like_array(list):
	def __mul__(self, other):
		return numpy_like_array([element*other for element in self])


UP = numpy_like_array([0, 1, 0])
DOWN = numpy_like_array([0, -1, 0])
LEFT = numpy_like_array([-1, 0, 0])
RIGHT = numpy_like_array([1, 0, 0])
PI = _original_math.pi
TAU = 2*_original_math.pi










