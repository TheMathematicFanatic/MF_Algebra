from abc import ABC, abstractmethod


class MobHolderBase(ABC):
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
	@abstractmethod
	def get_mob_from_expression(cls, latex):
		pass



class AnimationHolder(ABC):
	pass

