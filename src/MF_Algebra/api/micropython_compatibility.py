import sys
from types import ModuleType


class _ModuleWrapper:
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

class _math(_ModuleWrapper):
	import math as _original_math
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


class _asteval(_ModuleWrapper):
	original_module = 'asteval'
sys.modules['asteval'] = _asteval()


class _tabulate(_ModuleWrapper):
	original_module = 'tabulate'
sys.modules['tabulate'] = _tabulate()


class _typing(_ModuleWrapper):
	original_module = 'typing'
	def __getattr__(self, name):
		class _fake_Literal_and_stuff:
			def __getitem__(self, item):
				return self
		return _fake_Literal_and_stuff()
sys.modules['typing'] = _typing()


class _copy(_ModuleWrapper):
	import copy as _original_copy
	original_module = _original_copy
	@staticmethod
	def deepcopy(obj, memo={}):
		pass
sys.modules['copy'] = _copy()

