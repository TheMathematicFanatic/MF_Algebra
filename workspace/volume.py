import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *
from MF_Tools import *


V,r,h = Variables('Vrh')

class VolumeScene(Scene):
	def construct(self):
		vals = {
			V: V,
			r: 1,
			h: 3
		}
		Real.decimal_places = 2
		self.equation = V | pi*r**2
		self.shape = Cylinder(radius=vals[r], height=vals[h])
		V_val = Solve(V,self.equation @ vals).solution
		self.timeline = self.equation >> substitute_(vals) >> Solve(V)
		self.timeline.get_vgroup().fix_in_frame().to_edge(UR)
		self.timeline.play_all(self)
		self.embed()