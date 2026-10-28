

class MobHolderBase:
	def __init__(self, expression):
		self.expression = expression
		self.mobject = self.__class__.get_mob_from_expression(expression)
		super().__init__()

	def __getattr__(self, name):
		try:
			mobject = self.__dict__['mobject']
		except:
			raise AttributeError(name)
		return getattr(mobject, name)
	
	@classmethod
	def get_mob_from_expression(cls, latex):
		pass

	def __len__(self):
		return len(self.mobject)



class AnimationHolderBase:
	pass





def decide_api_mode_from_env():
	import sys
	if sys.platform in ('emscripten', 'webassembly'):
		return 'Web'
	from importlib.util import find_spec
	if find_spec('manimlib'):
		return 'ManimGL'
	if find_spec('manim'):
		return 'ManimCE'
	if find_spec('bpy'):
		return 'Blender'
	return 'None'
