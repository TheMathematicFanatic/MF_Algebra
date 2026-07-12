import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Tools import *
from MF_Algebra import *



class YourMom(Scene):
	def construct(self):
		axes = Axes()
		dot = Dot()
		point = Point()
		Indicate