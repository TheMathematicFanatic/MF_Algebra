from .action_core import Action



class AddressMapAction(Action):
	def __init__(self, *addressmap, **kwargs):
		super().__init__(**kwargs)
		self.addressmap = addressmap

	def get_addressmap(self, input_expression, **kwargs):
		return self.addressmap


class GlyphMapAction(Action):
	def __init__(self,
		input_exp,
		output_exp,
		*glyphmap,
		**kwargs
		):
		action_kwargs = {
			key : kwargs.pop(key)
			for key in Action.__init__.__code__.co_varnames[1:]
			if key in kwargs
		}
		super().__init__(**action_kwargs)
		self.TBGM_kwargs = kwargs
		self.input_exp = input_exp
		self.output_exp = output_exp
		self.glyphmap = glyphmap
	
	def get_glyphmap(self, expA, expB, addressmap):
		return self.glyphmap

	def get_output_expression(self, input_expression):
		return self.output_exp


class AnimationAction(Action):
	def __init__(self, animation, **kwargs):
		super().__init__(**kwargs)
		self.animation = animation # callable on two mobjects
	
	def get_animation(self, **kwargs):
		def animation(self, input_exp, output_exp=None):
			if output_exp is None:
				output_exp = self.get_output_expression(input_exp)
			return self.animation(input_exp.mob, output_exp.mob, **kwargs)
		return animation
