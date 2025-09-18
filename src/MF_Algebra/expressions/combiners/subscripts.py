from .combiners import Combiner
from .operations import Operation


class Subscript(Combiner):
	def __init__(self, *children, **kwargs):
		super().__init__("_", 0, children=children, **kwargs)
	
	def auto_parentheses(self):
		for i,child in enumerate(self.children):
			if i==0 and isinstance(child, (Combiner, Operation)):
				child.give_parentheses()
			child.auto_parentheses()
		return self

	def is_variable(self):
		from ..variables import Variable
		# This is horrible we gotta find another way lol
		self.children[0].is_variable = lambda *args: False
		return isinstance(self, Variable) or isinstance(self.children[0], Variable)



class Subscriptable(type):
	# This was a cool idea but unfortunately I just can't get it to work.
	# I can really only forsee wanting it to work for Variables so I'll
	# achieve the goal from there.
	def __instancecheck__(cls, instance):
		# Just provides Subscript instances the ability to pass as their first child's type
		# That way x_3 counts as a Variable for example as far as isinstance(x_3, Variable)
		if super().__instancecheck__(instance):
			return True
		if isinstance(instance, Subscript):
			return isinstance(instance.children[0], cls)
		return False