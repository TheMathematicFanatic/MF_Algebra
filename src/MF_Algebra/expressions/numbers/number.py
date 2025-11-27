from ..expression_core import *
from ..combiners.operations import Div
import numpy as np


class Number(Expression):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.value = None

	def compute(self):
		return float(self)

	def __float__(self):
		return float(self.value)

	def hash_key(self):
		return (self.__class__, tuple(self.children), self.value)
