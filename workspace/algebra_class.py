import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *


algebra_config['always_color'] = {a:RED_B, b:GREEN_D, c:PURPLE, n:GOLD}
random.seed()

class CheckIdentity(Scene):
	def construct(self):
		identity = AlgebraicAction((a+b)**n, a**n + b**n, var_kwarg_dict={n:{"path_arc":PI/2}})
		self.restart(identity)
		self.embed()

	def restart(self, identity: AlgebraicAction):
		self.clear()
		self.identity = identity
		self.timeline = self.identity.template1 >> Timeline(auto_scale=2)
		for _ in range(1):
			self.timeline >>= self.identity
			self.timeline >>= self.identity.reverse()
		self.timeline >>= equals_(self.identity.template2)
		self.timeline.get_vgroup().move_to(UP)
		self.timeline.play_all(self)

	def check_values(self, var_dict=None):
		evaluate = Evaluate(self.timeline.get_expression(-1).copy().reset_caches(), auto_scale=2)
		if var_dict is None:
			var_dict = {var: random.randint(0,9) for var in self.identity.get_all_variables()}
		evaluate >>= substitute_(var_dict, lag=0.2, mode='swirl', maintain_color=True)
		evaluate.get_vgroup().next_to(self.timeline.mob, 2*DOWN)
		self.play(ReplacementTransform(self.timeline.mob.copy(), evaluate.mob))
		evaluate.play_all(self, wait_between=0.5)
		final_eq = evaluate.get_expression(-1)
		left,right = final_eq.children
		if left == right:
			result = Text('Seems legit!').set_color(GREEN_B).next_to(final_eq.mob, DOWN)
			self.play(Indicate(final_eq.mob, color=GREEN_B), Write(result))
		else:
			result = Text('So it is wrong...').set_color(RED_D).next_to(final_eq.mob, DOWN)
			self.play(Indicate(final_eq.mob, color=RED_D), Write(result))			
		self.wait()
		self.play(FadeOut(result), FadeOut(final_eq.mob))



