import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manimlib import *
from MF_Algebra import *


L,R = Variables('LR')
unwrap_arg = rewrap_subex_(f(x), x, x)



class SeriesTest(Scene):
	def construct(self):
		self.series = Sum(n,1,inf)((14/(n+1)))
		self.play(Write(self.series.mob))
		self.wait()
		self.embed()
		self.root_test()
	
	def root_test(self):
		title = TexText('Root Test').to_edge(UP)
		self.play(Write(title))

		root_timeline = (self.series
			>> unwrap_arg
			>> apply_func_(Rad(n))
			>> apply_func_(Limit(n,inf))
			>> equals_(R,'left')
			>> root_pow_().right()
		)
		root_timeline.play_all(self)

	def ratio_test(self):
		title = TexText('Ratio Test').to_edge(UP)
		self.play(Write(title))

		ratio_timeline = self.series >> unwrap_arg
		ratio_timeline >> mul_(ratio_timeline.exp) >> swap.right()
		n_ads = [ad for ad in ratio_timeline.exp.get_addresses_of_subex(n) if ad[0] == '1']
		ratio_timeline >> add_(1).pread(*n_ads)
		ratio_timeline >> apply_func_(abs_val) >> apply_func_(Limit(n,inf)) >> equals_(R,'left')
		ratio_timeline.play_all(self)
	
	def integral_test(self):
		title = TexText('Integral Test').to_edge(UP)
		self.play(Write(title))

		ratio_timeline = self.series >> ( AlgebraicAction(Sum(n,a,b)(z), Integral(a,b)(z*dx)) + substitute_({n:x}).right() )

		ratio_timeline.play_all(self)
	
	def nth_term_test(self):
		title = TexText('nth Term Test').to_edge(UP)
		self.play(Write(title))
		
		nth_term_timeline = self.series >> unwrap_arg >> apply_func_(Limit(n,inf))

		nth_term_timeline.play_all(self)

	def view_rectangles(self):
		pass