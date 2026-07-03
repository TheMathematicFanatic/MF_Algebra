import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from MF_Tools.dual_compatibility import *
from MF_Algebra import *


class MrMathFraction(Scene):
	def construct(self):
		a,b,c,d = 4,9,5,12
		frac1 = Div(a,b)
		frac2 = Div(c,d)
		exp = frac1 + frac2

		common_denominator = int(np.lcm(b,d))
		frac1_multiplier = common_denominator // b
		frac2_multiplier = common_denominator // d

		timeline = ( exp
			>> mul_(frac1_multiplier).pread('00','01')
			>> evaluate_().pread('00','01')
			>> mul_(frac2_multiplier).pread('10','11')
			>> evaluate_().pread('10','11')
			>> dist_div_add_().reverse()
			>> evaluate_().pread('0')
			>> equals_(exp, side='left')
		)
		timeline.get_vgroup().scale(3)

		timeline.play_all(self)
		self.wait(3)



class MrMathCirclePEMDAS(Scene):
	def construct(self):
		algebra_config['default_color'] = BLACK
		algebra_config['multiplication_mode'] = 'dot'
		exp = (150**two - 140**two) / (5**two + 2**two)
		timeline = Evaluate(auto_scale=2).suspend()
		timeline >> exp
		self.play(Write(timeline.mob))
		self.wait()
		while timeline.exp.children:
			act = timeline.decide_next_action(timeline.current_exp_index)
			address = act.preaddress
			subex_mob = timeline.exp[address]
			circle = Ellipse(width=subex_mob.get_width(), height=subex_mob.get_height())
			circle.move_to(subex_mob).scale(1.4).set_color(GREEN_E)
			self.play(ShowCreation(circle))
			timeline >> act
			animation = timeline.get_animation(timeline.current_exp_index)
			timeline.current_exp_index += 1
			self.play(animation, FadeOut(circle, run_time=0.5))
			self.wait()
		timeline >> equals_(exp, side='left')
		timeline.play_next(self)
		self.wait()