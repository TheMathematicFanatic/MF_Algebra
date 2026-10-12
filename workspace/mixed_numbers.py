if __name__ == '__main__':
	from ..src.MF_Algebra import *	
else:
	import sys
	import os
	# Add the src directory to the sys.path
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
	from MF_Tools.dual_compatibility import *
	from MF_Algebra import *




class MixedNumber(SilentAdd):
	# string_code = [
	# 	child(0),   # This is a great idea
	# 	"\\tfrac{", # because from anywhere I can
	# 	child(1,0), # override the glyphs and
	# 	",",        # strings without needing to
	# 	child(1,1), # override the tree!
	# 	"}"
	# ]
	def __init__(self, W, N, D):
		self.W = Smarten(W)
		self.N = Smarten(N)
		self.D = Smarten(D)
		super().__init__(W, Div(N,D))
	
	def to_improper_timeline(self) -> Timeline:
		T = Timeline()
		T >> AlgebraicAction(SilentAdd(a,b),Add(a,b),['+','+'])
		T >> div_(1).left()
		T >> mul_(self.D).pread('00','01')
		T >> evaluate_().pread('00','01')
		T >> dist_div_add_().reverse()
		T >> evaluate_().pread('0')
		return T
		



class NewScene(Scene):
	def construct(self):
		A = MixedNumber(5,3,11)
		B = MixedNumber(7,2,9)
		T = Timeline() >> (A + B)

		# to_improper = Timeline()
		# T >> to_improper().both()
		# T >> A.to_improper_timeline().pread('0')
		# T >> B.to_improper_timeline().pread('1')
		for act in A.to_improper_timeline().actions:
			T >> act.pread('0')
		for act in B.to_improper_timeline().actions:
			T >> act.pread('1')
		
		a_den = T.expressions[-1].get_subex('01').compute()
		b_den = T.expressions[-1].get_subex('11').compute()
		import math
		lcm = math.lcm(a_den, b_den)
		a_mul = lcm // a_den
		b_mul = lcm // b_den

		T >> (mul_(a_mul).pread('00', '01') | mul_(b_mul).pread('10', '11'))
		T >> evaluate_().pread('00', '01', '10', '11')
		T >> dist_div_add_().reverse()
		T >> evaluate_().pread('0')

		num = T.expressions[-1].get_subex('0').compute()
		den = T.expressions[-1].get_subex('1').compute()

		W = num // den
		N = num % den

		T >> replace_with_(Add(num-N, N)).pread('0')
		T >> dist_div_add_()
		T >> replace_with_(Mul(W,den)).pread('00')
		T >> mul_div_R_().pread('0')
		T >> AlgebraicAction(Add(a,b),SilentAdd(a,b),['+','+'])

		
		self.embed()


random_bool_exp