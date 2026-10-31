
class Factory:
	def __init__(self, make_func):
		self.make_func = make_func


class CoolBase:
	def __init__(self, **kwargs):
		cls = type(self)
		names = []
		for name in dir(cls):
			if name.startswith('_'):
				continue
			value = getattr(cls, name)
			if callable(value) or isinstance(value, property):
				continue
			names.append(name)
		for key in kwargs:
			if key not in names:
				raise TypeError(f"{cls.__name__}.__init__() got an unexpected keyword argument '{key}'")
		for name in names:
			if name in kwargs:
				value = kwargs[name]
			else:
				value = getattr(cls, name)
				if isinstance(value, Factory):
					value = value.make_func()
			setattr(self, name, value)
	


