from abc import ABC, abstractclassmethod


class MobHolderBase(ABC):
	def __init__(self, expression):
		self.expression = expression
		self.mobject = self.__class__.get_mob_from_expression(expression)

	def __getattr__(self, name):
		return getattr(self.mobject, name)
	
	@abstractclassmethod
	def get_mob_from_expression(cls, latex):
		pass



class AnimationHolder(ABC):
	pass

