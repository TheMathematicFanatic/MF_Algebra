import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *




upper_series = Series((sin(pi/6))**n)
upper = Integral(0, inf, vertical_bounds=True)(Div(1,2) * upper_series * du)

lower_series = Series(((-1)**n * t**(2*n+1)) / (fact(2*n+1)))
lower_lower = -fact(3)/pi * Series(1/n**2, n, 1)
lower = Integral(lower_lower, pi/2, vertical_bounds=True)(lower_series * dt)

trig_frac = ( (sin**2)(t) + (cos**2)(t) ) / ( (sin**2)(t) + (cos**(e**ln(2)))(t) )
denom_base = d/dt * (t+ln(trig_frac)) + x**2
denom_pow = Series(2/(n*(n+1)), n, 1)
frac = arctan(x) / denom_base**denom_pow

full = Integral(lower, upper, vertical_bounds=True)(frac * dx)


algebra_config['always_color'] = {x:RED,y:BLUE,w:PURPLE,z:GREEN_E}
class SelectionScene(InteractiveScene):
	actions_to_try = [
		evaluate_(),
		swap_children_(),
		AlgebraicAction((a/b)**n, (b/a)**-n, [[], '1-']),
		AlgebraicAction((sin**2)(t) + (cos**2)(t), 1, ['', '']),
		AlgebraicAction(Taylor(sin(t),t), sin(t), ['', '']),
		AlgebraicAction((x+h)**3, x**3 + 3*x**2*h + 3*x*h**2 + h**3),
		AlgebraicAction((x-h)**3, x**3 - 3*x**2*h + 3*x*h**2 - h**3),
	]
	for rule in EquationManeuver.__subclasses__():
		actions_to_try += [
			rule(),
			rule().reverse(),
			rule().flip(),
			rule().reverse_flip()
		]
	for rule in SimplificationRule.__subclasses__():
		for subrule in [rule(), rule().reverse()]:
			if not subrule.template1 == a:
				actions_to_try.append(subrule)
	keep_selected_address_after_action = True
	
	def construct(self):

		self.new_timeline(
			# Limit(h,0)(	( f(x+h) - f(x) ) / h )
			x | 3
		)

		self.embed()

	def new_timeline(self, exp):
		self.clear()
		self.timeline = Timeline(auto_fit=[10,4,None])
		self.timeline >> exp
		self.timeline.play_all(self)

	def get_highlight(self, mobject: Mobject) -> Mobject:
		return Mobject() # default glow is not performant
	
	def gather_new_selection(self):
		super().gather_new_selection()
		if self.readied_action:
			self.apply_action_at_selection(self.readied_action)
			if self.mode != 'reload':
				self.readied_action = None
		else:
			self.get_working_actions()

	def get_working_actions(self):
		address = self.get_address_from_selection()
		self.timeline.exp.mob.set_color(WHITE)
		self.timeline.exp.set_color_by_subex(self.timeline.auto_color)
		self.timeline.exp[address + '_'].set_color(GREEN)
		subex = self.get_subex_from_selection()

		self.working_actions = []
		i = 0
		print('--- Subexpression ---')
		print(subex)
		print('--- Working Actions ---')
		for action in self.actions_to_try:
			try:
				output = subex >= action
				print(f'({i}) Action: ', action)
				print('    Output: ', output)
				print('')
				self.working_actions.append(action)
				i += 1
			except:
				pass

	def get_address_from_selection(self, expression=None) -> Address:
		expression:Expression = expression or self.timeline.exp
		selected_glyphs = [i for i in range(len(expression.mob)) if expression.mob[i] in self.selection]
		addressbook = expression.get_addressbook()
		for address, glyphs in addressbook.items():
			if selected_glyphs == glyphs:
				return address.removesuffix('_')
		return None
	
	def get_subex_from_selection(self, expression=None) -> Expression:
		expression = expression or self.timeline.exp
		address = self.get_address_from_selection(expression)
		if address is None:
			return None
		return expression.get_subex(address)
	
	def apply_action_at_address(self, action, address):
		self.timeline >> action.pread(address)
		self.timeline.play_all(self)
		self.save_state()

	def apply_action_at_selection(self, action):
		if len(self.selection) == 0:
			address = ''
		else:
			address = self.get_address_from_selection()
		self.apply_action_at_address(action, address)
		self.clear_selection()
	
	def __rshift__(self, other):
		if isinstance(other, int):
			other = self.working_actions[other]
		self.apply_action_at_selection(other)
		return self
	
	def ready_action(self, action):
		# while not self.selection:
			# pass
		self.apply_action_at_selection(action)

	def save_timeline(self, filename):
		self.timeline.reset()
		save_to_file(self.timeline, filename)

	def load_timeline(self, filename):
		self.clear()
		self.timeline = load_from_file(filename)
		assert isinstance(self.timeline, Timeline)
		self.timeline.play_all(self)

	def view_ladder(self):
		self.save_state()
		self.clear()
		self.timeline.reset_caches() # For some reason animations are permanently
		# altering the locations of some glyphs, need to look into this.
		self.add(self.timeline.get_mob_ladder()),

	def setup(self, *args, **kwargs):
		super().setup(*args, **kwargs)
		self.mode = 'normal'
		self.readied_action = None
		self.toggle_selection_mode()

	def ready_action(self, action, always=False):
		self.readied_action = action
		if always:
			self.mode = 'reload'

	def undo(self):
		self.timeline.undo_last_action()
		super().undo()



class SolveSelected(SelectionScene):
	def construct(self):
		self.timeline = Solve(t)
		self.solve_color = GREEN
		# eq = a | b**n + x/y
		t0 = Variable('t_0', 2)
		eq = t | t0 / sqrt(1-v**2/c**2)
		self.timeline >> eq
		self.timeline.play_all(self)




		self.embed()
	
	def solve_for_selected(self):
		solve_for = self.get_subex_from_selection()
		self.clear_selection()
		self.timeline.exp[solve_for].set_color(self.solve_color)
		self.timeline.auto_color = {solve_for: self.solve_color}
		self.timeline.set_solve_for(solve_for)
		self.timeline.play_all(self)
	
	def apply_action(self, action):
		self.timeline >> action
		self.timeline.play_all(self)
	
	def __rrshift__(self, action):
		self.apply_action(action)


pyth = (sin**2)(t) + (cos**2)(t)



class replace_with_(Action):
	def __init__(self, expression, **kwargs):
		self.expression = expression
		super().__init__(**kwargs)
	
	def get_output_expression(self, input_expression):
		return self.expression
	
	def get_addressmap(self, input_expression=None):
		return [['', '']]



class ZoomSelected(SelectionScene):
	save_stack = []
	def construct(self):
		# algebra_config['multiplication_mode'] = 'dot'
		self.timeline = Timeline(auto_fit=[10,6,None])
		self.timeline >> full
		self.timeline.play_all(self)
		self.embed()
	

	def zoom_to_selected(self, address=None):
		if address is None:
			address = self.get_address_from_selection()
		expression = self.timeline.exp.get_subex(address)
		self.clear_selection()
		self.save_stack.append((self.timeline.exp.copy(), address))
		self.timeline >> unwrap_subex_(self.timeline.exp, expression)
		self.timeline.play_all(self)


	def restore_to_original(self):
		self.clear_selection()
		v = Variable('temp')
		exp, ad = self.save_stack.pop()
		stripped_exp = exp.substitute_at_address(v, ad)
		self.timeline >> substitute_into_(stripped_exp, v)
		self.timeline.play_all(self)


	def work_selected(self):
		selected_subex = self.get_subex_from_selection()

		if selected_subex == upper:
			self.upper()
		elif selected_subex == lower_lower:		
			self.lower_lower()
		elif selected_subex == lower_series:
			self.lower_series()
		elif selected_subex == trig_frac:
			self.trig_frac()
		else:
			print("I didn't make that one lol")

	@staticmethod
	def zoom_decorator(subex):
		"""Decorator factory that takes a subex and returns a decorator."""
		# print('zoom_decorator')
		def decorator(func):
			# print('decorator')
			def wrapper(self, *args, **kwargs):
				# print('wrapper')
				# Get address and zoom
				address = self.timeline.exp.get_addresses_of_subex(subex)[0]
				print(address)
				self.zoom_to_selected(address)
				
				# Call the original method
				result = func(self, *args, **kwargs)

				# Play the timeline
				self.timeline.play_all(self)
				
				# Restore
				self.restore_to_original()
				return result
			return wrapper
		return decorator

	@zoom_decorator(lower_lower)
	def lower_lower(self):
		self.timeline >> substitute_({Sum(n,1,inf)(1/n**2):pi**2/6})
		self.timeline >> evaluate_().pread('00') >> replace_with_(-pi)

	@zoom_decorator(lower_series)
	def lower_series(self):
		self.timeline >> rewrap_subex_(self.timeline.exp, sin(t), t)

	@zoom_decorator(trig_frac)
	def trig_frac(self):
		self.timeline >> AlgebraicAction(e**ln(a), a).pread('1101') >> substitute_({pyth:1}) >> evaluate_()
	

	def denom_base(self):
		pass


	def upper(self):
		address1 = self.timeline.exp.get_addresses_of_subex(upper)[0]
		self.zoom_to_selected(address1)
		address2 = self.timeline.exp.get_addresses_of_subex(upper_series)[0]
		self.zoom_to_selected(address2)
		self.timeline >> substitute_({sin(pi/6):1/two}) #>> rw >> evaluate_()
		self.restore_to_original()
		self.timeline >> unwrap_subex_(self.timeline.exp, inf)
		self.restore_to_original()



# FOIL = AlgebraicAction(
# 	(a+b)*(x+y),
# 	a*x + a*y + b*x + b*y,
# 	['0+', []], ['1+', []], [[],'+'],
# 	var_kwarg_dict = {v:{'path_arc':PI} for v in (a,b,x,y)},
# )


from itertools import product

class FOIL(Action):
	path_arc = 3
	def get_output_expression(self, input_expression):
		if not isinstance(input_expression, Mul):
			print(type(input_expression))
			raise IncompatibleExpression
		return Add(*[
			Mul(*term_combination)
			for term_combination in product(*[
				child.children if isinstance(child, Add) else [child]
				for child in input_expression.children
			])
		])
	
	def get_addressmap(self, input_expression, **kwargs):
		addressmap = []
		for i, child in enumerate(input_expression.children):
			siblings = input_expression.children[:i] + input_expression.children[i+1:]
			for j, grandchild in enumerate(child.children):
				addressmap += [
					[f'{i}{j}', f'{k}{i}', {'path_arc':self.path_arc}]
					for k in range(n)
				]
		return addressmap
		


class PlayTimeline(Scene):
	def construct(self):
		timeline = load_from_file('test2')
		timeline.play_all(self, wait_between=0.5)



class plug_in_bounds_(Action):
	def get_output_expression(self, input_expression):
		assert isinstance(input_expression, ApplyFunction)
		assert isinstance(input_expression.left, PlugInBounds)
		return input_expression.expand_on_args()
	
	def get_addressmap(self, input_expression, **kwargs):
		return [
			['1'] # fuck man idk
		]



class CalcPrepIntegral(SelectionScene):
	def construct(self):
		self.timeline = Timeline()
		self.timeline >> Integral(0,inf)((e**x / (e**(2*x)+1))*dx)
		self.add(self.timeline.mob)

		anti = GlyphMapAction(
			Integral(0,inf)(1 / (1+x**2) * dx),
			PlugInBounds(0,inf,x)(arctan(x)),
			([0],[9,10,11]),
			([2],[13]),
			([1],[12]),
			([7],[7]),
			auto_morph = True,
			auto_resolve_kwargs = {'path_arc':1, 'delay':0.1, 'lag_ratio':0.03}
		)

		self.actions_to_try = [
			anti,
			sub_self := AlgebraicAction(PlugInBounds(a,b,x)(y), y-y, ['0f', '-']),
			swap := swap_children_(),
			u_sub := substitute_({0:1,e**x*dx:du,e**x:u}),
			ppr := pow_pow().reverse(),
			move_numer := AlgebraicAction(a/b*c, 1/b * (a*c), [FadeIn, '00'])
		]

		self.embed()



class Uwezi(SelectionScene):
	def construct(self):
		A,B,C,x,y,i,n = Variables('ABCxyin')
		xi = Subscript(x,i)
		yi = Subscript(y,i)
		S = Sum(i,0,n)
		eq = S(A*(xi*yi)) | S(B*xi**2) + S(C*xi)
		
		linear = AlgebraicAction(
			f(a*x),
			a*f(x),
			var_kwarg_dict = {a:{'path_arc':PI/2}}
		)

		

		self.timeline = Timeline(auto_fit=[8,4,None],auto_color={x:RED,y:BLUE})
		self.timeline >> eq
		self.add(self.timeline.mob)
		self.embed()


class TikTokSolve(SelectionScene):
	def construct(self):
		self.text_top = VGroup(
			Text('Can you find the solution?')
		).arrange(DOWN).to_edge(UP)
		self.text_bottom = VGroup(
			Text('MF_Algebra - a Manim plugin for automatic algebra'),
			Text('Code on Github, same username')
		).arrange(DOWN).scale(0.75).to_edge(DOWN)
		# self.new_equation(full)
		self.embed()


	def new_equation(self, equation, solve_for=None):
		if hasattr(self, 'timeline'): self.remove(self.timeline.mob)
		self.timeline = Solve(solve_for=solve_for, auto_fit=[8,6,None]).suspend()
		self.timeline >> equation
		self.play(Write(self.timeline.mob))
		if self.text_bottom not in self.mobjects:
			self.play(Write(self.text_bottom))
	
	def solve_equation(self):
		self.timeline.resume()
		self.timeline.play_all(self)
		
	def test_solution(self, value=None):
		if value is None:
			value = self.timeline.solution
		eq = self.timeline.exp
		var = eq.get_all_variables().pop()
		self.remove(self.timeline.mob)
		self.timeline = Evaluate(auto_fit=[8,6,None]) >> eq >> substitute_({var:value})
		self.add(self.timeline.mob)
		self.timeline.play_all(self)
		final_eq = self.timeline.exp
		if final_eq.compute():
			self.play(self.timeline.mob.animate.set_color(GREEN))
		else:
			self.play(self.timeline.mob.animate.set_color(RED))
		self.wait()
		self.remove(self.timeline.mob)
		self.new_equation(eq)



class MathScribblesTrigIntegral(SelectionScene):
	def construct(self):
		integral = I(x/sqrt(x**2+2*x+10)*dx)

		self.timeline = Timeline(auto_fit=[8,4,None],auto_color={x:RED,y:BLUE})
		self.timeline >> integral
		self.add(self.timeline.mob)
		self.embed()




def random_equation(depth=1):
	# import random
	random.seed()
	var = random.choice(list(algebra_config['always_color'].keys()))
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
	solution = random.choice(range(0,21))
	other = exp.copy().substitute({var:solution}).compute()
	exp = Equation(exp, other)
	return exp



class MathScribbles27(SelectionScene):
	def construct(self):
		lower1 = Limit(u,inf)((1+1/u)**u)
		lower2 = Sum(n,0,inf)(1/fact(n))
		lower = lower1 - lower2

		upper1 = Integral(-inf,inf)(e**(-u**2)*d(u))
		upper2 = Integral(0,2)((3/two*w**2-w)*d(w))
		upper = upper1**2 * upper2

		num1 = (cos**(9/pi*(tan**-1)(sqrt(3))))(t)
		num2 = cos(t)*(sin**2)(t)
		den1 = (cos**(8/pi*(tan**-1)(1)))(t)
		den2 = (sin**(4*pi*(sin**-1)(1)))(t)
		frac = (num1 + num2)/(den1 + den2)
		
		inner_int = Integral(400,x)(frac**fact(2)*dt)

		integrand = Taylor(sin)**2 * (d/dx)(inner_int)

		full = Integral(lower, upper)(integrand*dx)
	
		self.timeline = Timeline(auto_fit=[12,4,None])
		self.timeline >> full
		self.timeline.play_all(self)
		self.embed()



class GraphScene(SelectionScene):
	def construct(self):
		self.timeline = Timeline()
		self.timeline >> Equation(f(x), x)
		NP = NumberPlane()
		graph = always_redraw(lambda: NP.get_graph(
			lambda x1: self.timeline.exp.right.substitute({x:x1}).compute(),
		))
		self.add(NP,graph)
		self.add(self.timeline.mob)
		self.embed()


class ChestnutIntegral(SelectionScene):
	def construct(self):
		numerator = 1 + (x**2*e**x + e**x)
		denominator = x**2 + 1
		problem = Integral(0,2)((numerator/denominator)*dx)
		self.timeline = Timeline() >> problem
		self.embed()


