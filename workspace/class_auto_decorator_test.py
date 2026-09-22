class Parent:
	def what_the_func(self, value):
		print(f'The value is: {value}')
	
	def deco1(func):
		def wrapper(*args, **kwargs):
			print("deco1 applied before")
			func(*args, **kwargs)
			print("deco1 applied after")
		return wrapper
	
	def deco2(func):
		def wrapper(*args, **kwargs):
			print("deco2 applied before")
			func(*args, **kwargs)
			print("deco2 applied after")
		return wrapper

	def deco3(func):
		def wrapper(*args, **kwargs):
			print("deco3 applied before")
			func(*args, **kwargs)
			print("deco3 applied after")
		return wrapper
	
	decorum = (deco1, deco2, deco3)
	
	def __init_subclass__(cls):
		func = cls.what_the_func
		original = getattr(func, '_original', func)
		func = original
		for deco in cls.decorum:
			func = deco(func)
		func._original = original
		cls.what_the_func = func
	
	
class Child(Parent):
	def what_the_func(self, value):
		print(f'This descendant\'s value is: {value}')

class Grandchild(Child):
	pass

class OtherGrandchild(Child):
	decorum = (Parent.deco1, Parent.deco3)


print('-----')
Carl = Parent()
Carl.what_the_func(45)
print('-----')
carl = Child()
carl.what_the_func(47)
print('-----')
ccarl = Grandchild()
ccarl.what_the_func(94)
print('-----')
ccurl = OtherGrandchild()
ccurl.what_the_func(13)
ccurl.what_the_func._original(ccurl, 49)
print('-----')
