class BaseClass:
	decorators = ['is_lovely']

	@staticmethod
	def is_lovely(func):
		def wrapper(*args, **kwargs):
			output = func(*args, **kwargs)
			return output + ' is lovely'
		return wrapper
	
	@staticmethod
	def is_so_fat(func):
		def wrapper(*args, **kwargs):
			output = func(*args, **kwargs)
			return output + ' is so fat'
		return wrapper

	def yo_mama(self, parent='parent of ambiguous gender'):
		return f'Yo {parent}'

	def __init__(self):
		if not getattr(self, '_is_decorated', False):
			self._is_decorated = True
			yo_mama = self.yo_mama
			for deco_name in self.decorators:
				decorator = getattr(self, deco_name)
				yo_mama = decorator(yo_mama)
			self.yo_mama = yo_mama



class ChildClass(BaseClass):
	decorators = ['is_so_fat', 'is_lovely']
	def yo_mama(self, parent='mama'):
		return super().yo_mama(parent)


class GrandchildClass(ChildClass):
	decorators = ['is_so_fat']
	pass


Janet = ChildClass()
print(Janet.yo_mama())


Eugenia = BaseClass()
print(Eugenia.yo_mama())

Ivan = GrandchildClass()
print(Ivan.yo_mama())
