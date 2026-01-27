from ..expression_core import *
import numpy as np


class Number(Expression):
	value_type = None
	def __init__(self, value, **kwargs):
		assert isinstance(value, self.value_type)
		super().__init__(**kwargs)
		self.value = value

	def compute(self):
		return self.value_type(self.value)

	def __float__(self):
		return float(self.value)
	
	def __int__(self):
		return int(self.value)

	def hash_key(self):
		return (self.__class__, tuple(self.children), self.value)
