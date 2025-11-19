import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *



class Interactive(Scene):
	def construct(self):
		A = x**2 + y**2
		SwapTest = swap_children_()
		swap0 = swap_children_(preaddress="0")
		swap1 = swap_children_(preaddress="1")
		div = div_(z)
		div0 = div_(z, preaddress="0")
		div1 = div_(z, preaddress="1")
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


class JadenPEMDAS(Scene):
	def construct(self):
		A = Div(Add(-5,1),2,mode='inline')**2-abs_value(-7)
		E = A >> Evaluate(auto_scale=2)
		E.get_vgroup().set_color(BLACK)
		E.play_all(self)
		self.embed()


class MathGuy(Scene):
	def construct(self):
		A = x-3 | 1
		S = Solve(auto_scale=2)
		self.embed()


class Simplifying(Scene):
	def construct(self):
		A = x**2 + y**2
		T = Timeline()
		T >>= A
		self.add(T.mob)
		aL = add_zero_L().pread('10')
		aLr = add_zero_L().pread('10').reverse()
		T >>= aLr
		T >>= aL
		self.embed()



class Culmination(Scene):
	def construct(self):
		S = Solve(auto_scale=2)
		S >>= x+4 | 10
		S >> add_(5).both()
		S >> div_(2).both()
		S >> pow_(2).both()
		S >> substitute_into_(1/(1-x)).both()
		S.play_all(self)
		self.embed()


class Culmination2(Scene):
	def construct(self):
		question1 = 'What is your name?'
		Question1 = TexText(question1)
		self.play(Write(Question1))
		name = input(question1 + '     ')
		var = Variable(name)

		question2 = 'What is your favorite number?'
		Question2 = TexText(question2)
		self.play(FadeOut(Question1, run_time=0.25), Write(Question2))
		num = input(question2 + '     ')
		num = Smarten(eval(num))
		self.play(FadeOut(Question2))

		S = Solve(auto_scale=2) >> Equation(var, num)
		self.play(Write(S.mob))
		S >> add_(1).both() >> add_(10).both() >> sub_(1).both()
		S.play_all(self)
		S >> mul_(2).both() >> mul_(5).both() >> div_(10).both()
		S.play_all(self)
		S.suspend() >> pow_(2).both() >> AlgebraicAction(a**2, a*a).both() >> AlgebraicAction(a*a, a**2).pread('0')
		S.play_all(self)
		S.resume()
		S.suspend() >> div_(1, side='left').both() >> evaluate_().pread('1')
		S >> div_(1, side='left').both() >> AlgebraicAction(1/(1/a), a).pread('0')
		S.play_all(self)
		S.resume()
		S >> pow_(3, side='left').both()
		S.suspend() >> mul_(0).both() >> mul_zero_R().both()
		S.play_all(self)
		S.resume() >> add_(5).both() >> pow_(3).both()
		S.play_all(self)
		S.suspend() >> var >> substitute_({var:num}, mode='swirl', run_time=3)
		S.play_all(self)	
		self.embed()

algebra_config['multiplication_mode'] = 'dot'
class TimelineSceneTest(TimelineScene):
	def construct(self):
		global algebra_config
		algebra_config['auto_color'] = {x:RED, y:BLUE}
		# ?? Why does this not work... pretty annoying
		self.timeline = Solve(auto_color={x:RED, y:BLUE, z:GREEN}, auto_scale=2)
		self & (3*x-4 | 30)
		self.embed()


class Relativity(TimelineScene):
	def construct(self):
		m1 = Variable("m'", 2)
		self.timeline = Solve(solve_for=m1, auto_color={v:GREEN, c:BLUE_E})
		self & (m1 | gamma * m)
		self & substitute_({gamma: 1/sqrt(1-v**2/c**2)})
		self.timeline.set_solve_for(v/c)
		self.timeline.play_all(self)
		self & AlgebraicAction(a**c/b**c, (a/b)**c).pread('0')
		self.timeline.set_solve_for(v)
		self.timeline.play_all(self)
 

class LimitRational(Scene):
	def construct(self):
		num_roots = [-1,-9]
		den_roots = [-1,-5,-8]
		lim_value = inf

		def factor_from_root(a):
			if a == 0:
				return x
			elif a > 0:
				return x-a
			elif a < 0:
				return x+abs(a)

		def get_term(coef, degree, var):
			coef = abs(coef)
			if degree == 0:
				return coef
			if coef == 1 and degree == 1:
				return var
			elif degree == 1:
				return coef*var
			elif coef == 1:
				return var**degree
			else:
				return coef*var**degree

		def expanded_from_roots(*roots):
			from sympy import Poly, prod
			from sympy.abc import y
			coefficients = Poly(prod(y - r for r in roots), y).all_coeffs()
			coefficients = [int(c) for c in coefficients]
			degree = len(coefficients) - 1
			expanded = get_term(coefficients[0], degree, x)
			for i in range(1, len(coefficients)):
				if coefficients[i] > 0:
					expanded += get_term(coefficients[i], degree-i, x)
				elif coefficients[i] < 0:
					expanded -= get_term(abs(coefficients[i]), degree-i, x)
			return expanded

		numerator_factored = Mul(*[factor_from_root(a) for a in num_roots])
		numerator_expanded = expanded_from_roots(*num_roots)
		denominator_factored = Mul(*[factor_from_root(a) for a in den_roots])
		denominator_expanded = expanded_from_roots(*den_roots)

		rational = numerator_expanded / denominator_expanded
		lim = Limit(x, lim_value)
		E = Evaluate(mode='all at once')
		E >> rational
		E >> apply_func_(lim)
		E >> equals_(rational)
		E >> substitute_({x:lim.destination}, mode='fade').pread('1')
		# self.embed(False)
		# E.expressions[-1].right.decimal_places = 10
		E.play_all(self)
		self.wait()
		self.embed()


class InteractiveSceneTest(InteractiveScene):
	def construct(self):
		T = Solve(auto_color={x:RED, y:BLUE, z:GREEN}, auto_scale=2)
		T >>= (3*x-4 | 30)
		self.embed()



class SeriesTest(Scene):
	def construct(self):
		self.set_series(4/(1+n**2))
		self.embed()

	def set_series(self, *args, **kwargs):
		self.clear()
		self.series = Series(*args, **kwargs)
		self.play(Write(self.series.mob))

	def show_terms(self):
		S = self.series
		terms_timeline = Evaluate(mode='all at once')
		S_with_terms = Equation(S, S.expand_on_args())
		terms_timeline >> S
		self.play(terms_timeline.mob.animate.move_to(S_with_terms['0']))
		terms_timeline >> equals_(S.expand_on_args())
		terms_timeline.play_all(self)
		self.wait()
		self.play(
			FadeOut(terms_timeline.exp['=1']),
			ReplacementTransform(terms_timeline.exp['0'], S.mob.center())
		)

	def divergence_test(self):
		S = self.series
		n = self.series.variable
		lim_timeline = Evaluate()
		lim_timeline >> S.term >> apply_func_(Limit(n, inf))
		lim_timeline >> equals_(S.term) >> substitute_({n:inf}).pread('1')
		lim_timeline.get_vgroup().shift(1.5*DOWN)

		self.play(
			S.mob.animate.shift(1.5*UP),
			ReplacementTransform(S['1_'].copy(), lim_timeline.mob)
		)
		lim_timeline.play_all(self, wait_between=0.5)
		result = lim_timeline.exp.right
		if isinstance(result, Number):
			if result.compute() == 0:
				color = GOLD
				result = TexText('Inconclusive...').set_color(color)
			else:
				color = RED_D
				result = TexText('Diverges!').set_color(color)
			self.wait()
			self.play(
				lim_timeline.mob.animate.set_color(color),
				S.mob.animate.set_color(color),
				Write(result)
			)
		else:
			pass
		self.wait()
		self.play(FadeOut(result), FadeOut(lim_timeline.mob), S.mob.animate.set_color(WHITE).center())


class LimScene(Scene):
	def construct(self):
		eq = Variable('L') | sqrt(h**2 + (f(x) - f(x+h))**2)
		lim = Limit(h,0)
		T = Timeline(auto_color={x:RED, h:PURPLE, f:BLUE, h**2:ORANGE}) >> eq >> apply_func_(lim).pread('1')
		T >> substitute_({x:15}, mode='swirl', maintain_color=True)
		T.play_all(self)


class SolveSimple(Scene):
	def construct(self):
		eqs = [
			3*x+5 | 14,
			6*w-4 | 12,
		]

algebra_config['multiplication_mode'] = 'auto'
algebra_config['always_color'] = {
	x:RED_D, y:BLUE_D, z:GREEN_D,
	a:RED_B, b:GREEN_D, c:BLUE_E,
	n:GOLD, m:BLUE_B, w:PURPLE, p:PINK,
	d: GREY_C,
	dx:RED_B, dy:BLUE_B, dz:GREEN_B,
}
class Differentiation(Scene):
	def construct(self, expression = x**3-5/z):
		D = Differentiate(auto_scale=2)
		D >>= expression
		D >> apply_func_(d)
		# D >> substitute_({a:3})
		# D.play_all(self)
		self.add(D.get_vgroup().arrange(DOWN, buff=1))
		self.embed()

	def reset(self, expression):
		self.clear()
		self.construct(expression)

# Differentiation().construct()


class SimplifyTesting(Scene):
	def construct(self):
		for SR_ in SimplificationRule.__subclasses__():
			name = Tex(str(SR_().template1) + ' \\to ' + str(SR_().template2))
			A = e**(x**2+y**2)
			input_expression = SR_().template1.substitute({a:A})
			T = input_expression >> SR_()
			self.play(
				Write(T.mob),
				FadeIn(name.to_edge(DOWN))
			)
			self.wait()
			T.play_all(self)
			self.play(*[FadeOut(mob) for mob in self.mobjects])


class DivideOrDistribute(Scene):
	def construct(self):
		eq = 3*(x+5) | 21
		distribute = AlgebraicAction(
			a*(b+c) | x,
			a*b + a*c | x,
			[[],'01*'],
			var_kwarg_dict={a:{'path_arc':-TAU/3}}
		)  # Couldn't figure out the preaddressing bug so I just included the RHS in the template lmao
		T1 = Solve().suspend()
		T1 >> eq >> distribute #.pread('0')
		T1.resume()

		frame = self.camera.frame
		frame.shift(DOWN*2)

		self.play(Write(T1.mob))
		self.wait()
		T1.play_all(self)
		
		T2 = Solve() >> eq
		self.play(ReplacementTransform(T1.mob, T2.mob))
		self.wait()
		T2.play_all(self)

		# distribute = GlyphMapAction(
		# 	([0], [0], {'path_arc':-PI/2}),
		# 	([0], [3], {'path_arc':-PI/2}),
		# 	([1,5], [], {'run_time':0.5}),
		# 	([], [4], {'run_time':0.5, 'delay':0.5}),
		# )
