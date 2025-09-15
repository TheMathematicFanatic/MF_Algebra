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
	
	def is_identical_to(self, other):
		other = Smarten(other)
		return type(self) == type(other) and self.value == other.value
