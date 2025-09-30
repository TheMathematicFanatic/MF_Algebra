import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *



class Interactive(Scene):
	def construct(self):
		A = x**2 + y**2
		s = swap_children_()
		s0 = swap_children_(preaddress="0")
		s1 = swap_children_(preaddress="1")
		d = div_(z)
		d0 = div_(z, preaddress="0")
		d1 = div_(z, preaddress="1")
		self.add(A.mob)
		self.embed()


class TimelineTest(Scene):
	def construct(self):
		A = x**2 + y**2
		s = swap_children_()
		s0 = swap_children_(preaddress="0")
		s1 = swap_children_(preaddress="1")
		d = div_(z)
		d0 = div_(z, preaddress="0")
		d1 = div_(z, preaddress="1")
		self.add(A.mob)
		T = Timeline()
		T.add_expression_to_end(A)
		T.add_action_to_end(s).add_action_to_end(s0).add_action_to_end(s1).add_action_to_end(s).add_action_to_end(d).add_action_to_end(s).add_action_to_end(d0).add_action_to_end(s0)
		T.propagate()
		self.embed()


class Theorem(Scene):
	def construct(self):
		A = Tex("x^2-4")
		B = Tex("(x-2)(x+2)")
		self.embed()


class CombineAnimations(Scene):
	def construct(self):
		A = Square()
		B = Circle()
		C = Text("Hello")

		AtoB = ReplacementTransform(A,B)
		BtoC = ReplacementTransform(B,C)
		AtoC = Succession(AtoB, BtoC)
		self.add(A)
		#self.play(AtoB)
		#self.play(BtoC)
		self.play(AtoC)
		self.embed()


class KeepGoin(Scene):
	def construct(self):
		A = x**2 + y**2
		self.add(A.mob)
		self.exp = A
		self.embed()


	def action_sequence(self):
		while True:
			action_name = input("Perform action: (or quit)\n>>> ")
			if 'quit' in action_name: break
			temp_locals = {}
			exec('action = ' + action_name, globals(), temp_locals)
			action = temp_locals['action']
			B = self.exp >= action
			self.play(action(self.exp, B))
			self.exp = B


class TreeTest(Scene):
	def construct(self):
		A = x**2 + y**2
		G = create_graph(A)
		A.mob.to_edge(LEFT)
		G.to_edge(RIGHT)
		self.add(A.mob,G)
		self.embed()


class EvaluateTest(Scene):
	def construct(self):
		A = x**2 + y**2
		A = A / (A**3 - A**2 + A)
		B = A >= substitute_({x:-3, y:4})
		E = Evaluate(B)
		self.add(E[0])
		for i in range(len(E)-1):
			self.play(E.actions[i](E.expressions[i], E.expressions[i+1]))
			self.wait()
		self.embed()


class TimelineTest2(Scene):
	def construct(self):
		T = Timeline()
		a**2 + b**2 >> T
		T >> div_(c**2)
		T >> add_(c**2, '1')
		T >> substitute_({a:15, b:8, c:17})
		T >> ( evaluate_('00') | evaluate_('01') | evaluate_('10') | evaluate_('11') )
		T >> ( evaluate_('0') | evaluate_('1') )
		T >> evaluate_()
		B = (1+x)/(1-x**2)
		T >> substitute_into_(B)
		T >> evaluate_('11')
		T >> ( evaluate_('0') | evaluate_('1') )
		T >> evaluate_()

		T.propagate()
		T.get_vgroup().scale(2.5)
		self.add(T.mob)
		T.play_all(self)


class TimelineTest3(Scene):
	def construct(self):
		T = Timeline()
		A = a**2 + b**2
		T >> substitute_({a:SmZ(4)-3, b:SmZ(5)-8})
		T >> evaluate_('00') >> evaluate_('10')
		T >> evaluate_('0') >> evaluate_('1')
		T >> evaluate_()

		self.add(A.mob)
		A >> T
		T.propagate()

		self.embed()
		

class TimelineTest4(Scene):
	def construct(self):
		T = AutoTimeline(auto_color={a:RED, b:GREEN, c:BLUE})
		A = a**2 + b**2
		A >> T
		T >> div_(c**2) >> add_((a/b)**2)
		T.propagate()
		self.add(A.mob)
		self.embed()


class FunctionSubstituteTest(Scene):
	def construct(self):
		F = f(x)
		A = y & x**2-5
		T = A >> ( substitute_into_(F, preaddress='0') | substitute_into_(F, preaddress='1') )
		T.propagate()
		self.add(T.mob)
		#self.embed()


class EvaluateTimelineTest(Scene):
	def construct(self):
		A = (a+b)/2 + (x+y)/25
		A = A.substitute({a:5, b:15, y:20})
		E = Evaluate(A, show_past_steps=True)
		self.add(E.mob)
		self.embed()


class ShowStepsTimelineTest(Scene):
	def construct(self):
		A = x**2 - y**2
		T = Evaluate(
			show_past_steps = True,
			auto_color = {x:RED, y:BLUE, e:GREEN, 3:YELLOW, -15:PURPLE}
		)
		A >> T >> div_(e**x-2+2) >> add_((x+y)**3) >> substitute_({x:1}) >> substitute_({y:4})
		self.play(Write(T.mob))
		T.play_all(self)
		self.play(self.camera.frame.animate.rotate(PI/3, RIGHT), run_time=3)
		self.wait()


class AlgebraicActionTest(Scene):
	def construct(self):
		A = x**2 + y**2
		T = Timeline()
		A >> T
		T >> AlgebraicAction(a+b, a/b)
		T >> AlgebraicAction(a/b, b/a)
		T >> AlgebraicAction(a/b, (b/a)**-1)
		T.propagate()
		self.add(T.mob)
		self.embed()


class EvaluateTimelineTest2(Scene):
	def construct(self):
		E = Evaluate(show_past_steps=True, auto_color={a:RED, b:GREEN, c:BLUE})
		a**2 + b**2 >> E
		E >> div_(c**2+3**a)
		E >> substitute_({a:3, b:4})
		E >> sub_(100, side='left')
		E >> substitute_({c:3})

		self.add(E.mob)
		self.embed()
		E.play_all(self)


class AlgebraTest(Scene):
	def construct(self):
		T = Evaluate(auto_color={x:RED, y:BLUE}, auto_scale=2.5, show_past_steps=True)
		(y & 2*x+4) >> T
		T >> swap_children_()
		T >> AlgebraMoves[0]
		T >> substitute_({y:100})
		#T >> evaluate_('1')
		T >> AlgebraMoves[2]
		#T >> evaluate_('1')

		self.play(Write(T.mob))
		self.wait()
		T.play_all(self)
		self.embed()


class AlgebraTest2(Scene):
	def construct(self):
		T = Timeline(auto_color={x:RED, y:BLUE}, auto_scale=2.5, show_past_steps=False, auto_propagate=False)
		(y & SmQ(1,2)*x+7) >> T
		T >> swap_children_()
		T >> substitute_({x:y, y:x})
		T >> AlgebraMoves[0]
		T >> AddressMapAction(
			['001', '10', {'path_arc':PI, 'delay':0}],
			['000', FadeOut, {'run_time':0.5}],
			['00/', FadeOut, {'run_time':0.5}],
			[FadeIn, '11()', {'delay':0.5}]
		) >> (y & 2*(x-7))
		T >> AddressMapAction(
			['10', '100', {'path_arc':-PI}],
			['10', '11', {'path_arc':-PI*0.75}],
			['111', '11'],
			['11()', FadeOut, {'run_time':0.5}]
		) >> (y & 2*x-14)
		# T >> substitute_({x:13})
		# T.propagate()
		# #T.get_expression(-1).get_subex('101').give_parentheses()
		# T >> evaluate_('10') >> evaluate_('1')
		T.propagate()
		
		self.play(Write(T.mob))
		self.wait()
		T.play_all(self, wait_between=0)
		self.embed()


class AlgebraTest3(Scene):
	def construct(self):
		T = Timeline(auto_color={x:RED, y:BLUE}, auto_scale=2.5, show_past_steps=False, auto_propagate=True)
		(y & (x+2)/(3*x+5)) >> T
		T >> swap_children_()
		T >> substitute_({x:y, y:x})
		T >> AlgebraMoves[3]
		# T.propagate()
		
		self.play(Write(T.mob))
		self.wait()
		T.play_all(self, wait_between=0)
		self.embed()


class AlgebraTest4(Scene):
	def construct(self):
		T = Evaluate(auto_color={a:RED, b:GREEN, c:PURPLE}, auto_scale=2.5, show_past_steps=False)
		(a**2 + b**2) >> T
		T >> div_(c**2)
		T >> substitute_({a:3, b:1, c:2}, mode='swirl', lag=0.3)
		T >> substitute_into_(x**2 + 1/(x+7))

		self.play(Write(T.mob))
		T.play_all(self, wait_between=0)
		self.embed()


class AlgebraTest5(Scene):
	def construct(self):
		act = alg_add_R
		exp = 4*x**3 + 12 & 9

		A = Timeline(auto_scale=2)
		exp.copy() >> A
		A >> act()
		A.get_vgroup().to_corner(UL)

		B = Timeline(auto_scale=2)
		act().get_output_expression(exp.copy()) >> B
		B >> act().reverse()
		B.get_vgroup().to_corner(UR)

		C = Timeline(auto_scale=2)
		swap_children_().get_output_expression(exp.copy()) >> C
		C >> act().flip()
		C.get_vgroup().to_edge(LEFT)

		D = Timeline(auto_scale=2)
		swap_children_().get_output_expression(act().get_output_expression(exp.copy())) >> D
		D >> act().reverse_flip()
		D.get_vgroup().to_edge(RIGHT)


	
		self.add(A.mob, B.mob, C.mob, D.mob)

		A.play_all(self)
		B.play_all(self)
		C.play_all(self)
		D.play_all(self)
	

class AlgebraTest6(Scene):
	def construct(self):
		act = alg_mul_L
		sub_dict = {a:3/(x**2+14*x-5), b:10*y*z, c:163}

		A = Timeline(auto_fit=[5,None,None])
		A_act = act()
		A_act.template1.copy().substitute(sub_dict) >> A >> A_act
		A.get_vgroup().to_corner(UL)

		B = Timeline(auto_fit=[5,None,None])
		B_act = act().reverse()
		B_act.template1.copy().substitute(sub_dict) >> B >> B_act
		B.get_vgroup().to_corner(UR)

		C = Timeline(auto_fit=[5,None,None])
		C_act = act().flip()
		C_act.template1.copy().substitute(sub_dict) >> C >> C_act
		C.get_vgroup().to_edge(LEFT)

		D = Timeline(auto_fit=[5,None,None])
		D_act = act().reverse_flip()
		D_act.template1.copy().substitute(sub_dict) >> D >> D_act
		D.get_vgroup().to_edge(RIGHT)

		
		self.add(A.mob, B.mob, C.mob, D.mob)
		for T in [A,B,C,D]:
			T.play_all(self)
		self.embed()
		

class AlgebraTest7(Scene):
	def construct(self):
		A = 4*x+5 & 21
		T = Evaluate(auto_scale=2.5)
		A >> T
		T >> alg_add_R()
		T >> alg_mul_L()

		self.play(Write(T.mob))
		T.play_all(self)
		self.embed()


class AlgebraTest8(Scene):
	def construct(self):
		A = 14-4*x & 25
		S = Solve(solve_for=x, auto_scale=2.5, auto_color={x:GREEN_E}, show_past_steps=True)
		A >> S
		S.play_all(self, wait_between=0)


class AlgebraTest9(Scene):
	def construct(self):
		A = a*x+b*y & c*z
		S = Solve(
			solve_for=y,
			auto_fit=[8,8,None],
			auto_color={x:RED, y:BLUE, z:GREEN}
		)
		A >> S
		S.play_all(self)
		self.embed()


class InteractiveAlgebra(Scene):
	def construct(self):
		A = a*x + b*y & c*z
		S = Solve(
			solve_for=y,
			auto_fit=[8,8,None],
			auto_color={x:RED, y:BLUE, z:GREEN}
		)
		A >> S
		S.play_all(self)
		S.set_solve_for(c)
		S.play_all(self)
		self.embed()


import random
class DeepEquation(Scene):
	def construct(self):
		random.seed()
		var = x
		depth = 5
		vars = [x,y,z]
		number_options = [1,5,8]
		S = Solve(
			solve_for = var,
			auto_fit = [8, 6, None],
			auto_color = {x:RED, y:BLUE, z:GREEN}
		)
		A = x
		vars.remove(var)
		for i in range(depth):
			if i == depth-1:
				OpClass = Equation
			else:
				OpClass = random.choice([Add, Sub, Mul, Div])
			side = random.choice(['left'])
			leaf_options = number_options + vars
			item = random.choice(leaf_options)
			if side == 'left':
				A = OpClass(item, A)
			elif side == 'right':
				A = OpClass(A, item)
		
		A >> S
		S.play_all(self)
		self.embed()
		S >> substitute_({v:random.choice(number_options) for v in vars})


class SolveTriangle(Scene):
	def construct(self):
		(alpha + (SmZ(30) + 60) & 180) >> (S := Solve(solve_for=alpha, auto_scale=2.5, auto_color={alpha:RED_A}))
		S.play_all(self, wait_between=0.5)
		self.embed()


class TestFunction(Scene):
	def construct(self):
		from MF_Algebra.extra.trigonometry import sin
		F = 3*sin(x/2)
		self.add(F.mob)
		self.embed()

	

class AutoParenTest(Scene):
	def construct(self):
		# alg = alg_mul_L().flip().reverse()
		# This is broken for some reason
		alg = alg_mul_L().reverse().flip()
		print(alg)
		T = (
			x**2 + y**2
			>> div_(x-4)
			>> equals_(x+4)
			>> alg
		)
		self.add(T.mob)
		self.embed()


class PlayingAround(Scene):
	def construct(self):
		E = a*x**2+b*y & c*z
		T = Solve(
			solve_for=x,
			auto_color={x:RED, y:BLUE, z:GREEN},
			auto_scale=3,
			show_past_steps=True,
		)
		E >> T
		T >> substitute_({a:3, b:4, c:5}, mode='swirl', lag=0.2)

		T.set_solve_for(z)
		T.solve_for = y
		T >> substitute_({x:-3, z:1})
		T.play_all(self)
		self.embed()


from MF_Algebra.extra.trigonometry import *
class TrigTest(Scene):
	def construct(self):
		A = (sin(x) + cos(pi/2-x)) / tan(x)
		T = Evaluate(auto_color={x:GREEN, pi:PURPLE}, auto_fit=[12, 6, None])
		A >> T

		T >> substitute_({x:pi/4})
		self.add(T.mob)
		T.play_next(self)
		self.embed()


class GlyphTesting(Scene):
	def construct(self):
		A = Integer(3)**3
		B = x**x
		C = sqrt(sqrt(sqrt(sqrt(sqrt(a/b)))))
		D = x**x**x**x**x**x**x
		self.add(VGroup(D.mob).arrange(RIGHT).scale(6))
		self.debug_glyphs(D.mob)
		self.wait(5)
	#self.embed()


class Coloring(Scene):
	def construct(self):
		T = Solve(auto_scale=3, auto_color={x:RED, y:BLUE, r:YELLOW, theta:GREEN})
		eqs = [
			x & r*cos(theta),
			y & r*sin(theta),
			tan(theta) & y/x,
			r**2 & x**2 + y**2,
		]
		T.auto_fill = False
		for eq in eqs:
			T.add_expression_to_end(eq)
		T.auto_fill = True
		T.resume()
		self.embed()


class BackgroundAlgebra(Scene):
	def construct(self):
		self.loop(1)
	
	def loop(self, number_of_times):
		for i in range(number_of_times):
			#try:
			T = self.generate_timeline()
			T.play_all(self)
			#except:
			#	pass
			if self.mobjects:
				self.play(FadeOut(Group(*self.mobjects)))

	def generate_timeline(self):
		A = Equation(random_number_expression(), random_number_expression())
		var_letter = random.choice('abcdfghjkmnpqrstuvwxyz')
		var = Variable(var_letter)
		var_color = random.choice([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE])
		S = Solve(
			solve_for=var,
			preferred_side='left',
			auto_color={var:var_color},
			auto_fit=[10, 6, None]
		)
		var_address = random.choice([ad for ad in A.get_all_addresses() if len(ad)>0])
		A = A.substitute_at_address(var, var_address)
		A >> S
		return S


class LogRules(Scene):
	def construct(self):
		S = Timeline(auto_scale=3, auto_color={x:RED, y:BLUE, e:GREEN, ln:PURPLE})
		A = e**x & y 
		A >> S
		self.embed()
		S.play_all(self)


from MF_Algebra.extra.calculus import *
class Derivative(Scene):
	def construct(self):
		algebra_config['multiplication_mode'] = 'dot'
		T = Timeline()
		d(x+y*z) >> T
		T >> SumRule >> ProductRule.pread('1')
		self.add(T.get_vgroup().arrange(DOWN))
		self.embed()





class MapleSyrup(Scene):
	def construct(self):
		A = Square().scale(3)
		B = Text("Hello Maple Syrup!")
		self.wait()
		self.play(Write(B), GrowFromCenter(A), run_time=3)
		self.embed()




class SwapTest(Scene):
	def construct(self):
		A = x**2 + y**2
		S = swap_children_()
		B = A >= S
		self.embed()


class RadGlyphTest(Scene):
	def construct(self):
		R = Rad(x)(4*x-f(x))
		R.get_glyphs_at_address('00')
		R.set_color_by_subex({x:RED, f:BLUE})
		self.add(R.mob)
		self.embed()











class SolvingPowerEquations(Scene):
	def construct(self):
		A = x**9 + 6**y | 3/(z**2+10)
		S = Solve(auto_scale=1.8, auto_color={x:RED, y:BLUE, z:GREEN})
		S = A >> S
		for v in x,y,z:
			S.set_solve_for(v)
			S.play_all(self)
		self.embed()


class EvaluatingFunctions(Scene):
	def construct(self):
		E = Evaluate()
		E = E >> Sum(n,0,5)(Log(n+2)(three**two+four**two))
		E = E >> E.get_expression(-1).expand_on_args()
		self.embed()


class MultSymbolTest(Scene):
	def construct(self):
		A = 3*x
		str(A)
		B = A @ {x:2}
		str(B)
		self.embed()


