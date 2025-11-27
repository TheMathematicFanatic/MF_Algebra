from ..expression_core import *
import numpy as np


class Number(Expression):
	value_type = None
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.value = None

	def compute(self):
		return float(self)

	def __float__(self):
		return float(self.value)
	
	def __int__(self):
		return int(self.value)

	def hash_key(self):
		return (self.__class__, tuple(self.children), self.value)
