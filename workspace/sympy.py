import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *


class TrySympy(Scene):
	def construct(self):
		A = x**2 + y**2
		As = A.to_sympy()
		self.embed()