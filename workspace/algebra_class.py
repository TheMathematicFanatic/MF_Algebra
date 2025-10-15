import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *
from MF_Tools import Vcis, scale_to_fit


# algebra_config['always_color'] = {a:RED_B, b:GREEN_D, c:PURPLE, n:GOLD}
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



class SolveEquation(Scene):
	def construct(self):
		self.reset_equation(x/4+5 | 12)
		self.embed()

	def reset_equation(self, equation):
		self.clear()
		self.equation = equation
		var = self.equation.get_all_variables().pop()
		algebra_config['always_color'] = {var:PURPLE}
		self.play(Write(self.equation.mob))

	def guess_solution(self, value):
		self.clear()
		timeline = Evaluate()
		timeline >>= self.equation
		self.add(timeline.mob)
		var = self.equation.get_all_variables().pop()
		timeline >>= substitute_({var: value}, maintain_color=True)
		timeline.play_all(self)
		self.wait()
		expr = timeline.get_expression(-1)
		L,R = expr.children
		if L == R:
			self.play(expr.mob.animate.set_color(GREEN))
		else:
			self.play(expr.mob.animate.set_color(RED))
		self.wait()
		self.play(FadeOut(timeline.mob))
		self.play(Write(self.equation.mob))

	def solve_equation(self, test=True):
		self.clear()
		timeline = Solve()
		timeline >>= self.equation
		self.add(timeline.mob)
		timeline.play_all(self)
		self.wait()
		self.play(FadeOut(timeline.mob))
		self.play(Write(self.equation.mob))
		if test:
			self.guess_solution(
				timeline.get_expression(-1).children[1]
			)


w = Variable('w', 1)
programmed_equations = [
	x+4 | 10,
	b+7 | 10,
	10-y | 9,
	20-a | 15,
	5*w | 55,
	4*z | 40,
	10*c | 80,
	n*2 | 14,
	87 + m | 100,
	3*p + 10 | 25
]
algebra_config['multiplication_mode'] = 'x'
algebra_config['always_color'] = {
	x:RED, y:BLUE, z:GREEN_E,
	a:RED_B, b:GREEN_D, c:BLUE_E,
	n:GOLD, m:BLUE_B, w:PURPLE, p:PINK
}

class EquationGame(Scene):
	def construct(self):
		self.mode = 'programmed'
		self.init_game(10)
		self.await_input()
		self.embed()

	def init_game(self, points_to_win):
		self.point_value = 0
		self.points_to_win = points_to_win
		self.point_indicators = VGroup(*[Circle().set_color(WHITE) for _ in range(points_to_win)])
		self.play(ShowCreation(self.point_indicators))
		self.wait(0.5)
		self.play(self.point_indicators.animate.arrange(RIGHT, buff=1).scale_to_fit(12).to_edge(UP), run_time=2)
		self.reset_equation()

	def await_input(self, recurse=True):
		print('')
		solution = input('What is the mystery number?    ')
		if solution == 'quit':
			return
		solution = eval(solution)
		solution = Smarten(solution)
		self.guess_solution(solution)
		if recurse and self.point_value < self.points_to_win:
			self.await_input(recurse=recurse)

	def reset_equation(self, equation=None, index=None):
		if hasattr(self, 'timeline'):
			self.play(FadeOut(self.timeline.mob))
		self.equation = equation
		if self.equation is None:
			if index is None:
				index = self.point_value
			if self.mode == 'programmed':
				self.equation = programmed_equations[index]
			elif self.mode == 'random':
				self.equation = random_equation()
			else: 
				print('Unknown mode: ', self.mode, '. Must be programmed or random.')
		self.timeline = Evaluate(auto_scale=2)
		self.timeline >>= self.equation
		self.play(Write(self.timeline.mob))

	def guess_solution(self, value):
		var = self.equation.get_all_variables().pop()
		self.timeline >>= substitute_({var: value}, maintain_color=True)
		self.timeline.play_all(self, wait_between=1)
		expr = self.timeline.get_expression(-1)
		L,R = expr.children
		if L == R:
			self.play(expr.mob.animate.set_color(GREEN))
			new_point_indicator = self.point_indicators[self.point_value].copy().set_fill(opacity=1, color=GREEN).set_stroke(opacity=0)
			self.play(ReplacementTransform(expr.mob, new_point_indicator))
			self.point_indicators[self.point_value].add(new_point_indicator)
			self.increment_point_value()
			self.reset_equation()
		else:
			self.play(expr.mob.animate.set_color(RED))
			self.reset_equation(equation=self.equation)

	def increment_point_value(self):
		self.point_value += 1
		if self.point_value >= self.points_to_win:
			self.you_win()

	def you_win(self):
		self.play(*[
			circ.animate.move_to(2.5*Vcis(TAU/self.points_to_win * i)).scale(1.1)
			for i,circ in enumerate(self.point_indicators)
		])
		always_rotate(self.point_indicators)
		self.wait()
		self.play(Write(TexText('You Win!')))
		self.wait(10)
		self.embed()

def random_equation(depth=2):
	import random
	var = random.choice([
		a,b,c,n,m,p,q,x,y,z
	])
	exp = var
	def one_more_layer(exp, OpClassList = [Add,Sub,Mul,Div,Pow]):
		OpClass = random.choice(OpClassList)
		side = random.choice(['left', 'right'])
		other = random.choice(range(0,21))
		if side == 'left':
			return OpClass(exp, other)
		elif side == 'right':
			return OpClass(other, exp)
	for i in range(depth):
		exp = one_more_layer(exp)
	solution = random.choice(range(-20,21))
	other = exp.copy().substitute({var:solution}).compute()
	exp = Equation(exp, other)
	return exp






exec

eval

