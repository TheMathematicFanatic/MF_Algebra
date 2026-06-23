import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from manimlib import *
from MF_Algebra import *


class Eml(BinaryOperation):
	symbol = '\\epsilon'
	symbol_glyph_length = 1
	eval_op = staticmethod(lambda x, y: np.exp(x) - np.log(y))

	def evaluate(self):
		x,y = self.children
		return e**x - ln(y)

	def auto_parentheses(self):
		for i, child in enumerate(self.children):
			if isinstance(child, (Add, Sub, Eml)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()
		return self


def matmul(self, other):
	return Eml(self, other)
Expression.__matmul__ = matmul



class EML_Scene(Scene):
	def construct(self):
		A = x@y
		E = Evaluate() >> A
		E.play_all(self)
		self.embed()