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



class SelectionScene(InteractiveScene):
	def construct(self):


		self.timeline = Timeline(auto_color={t:PURPLE,n:ORANGE,x:RED}, auto_scale=0.9)
		A = 1**x + y**1
		B = 3**b
		# self.timeline >> A/A + B - B
		# self.timeline >> Log(3)(3**x) + 3**Log(3)(y/5) + ln(e**9) + e**ln(15)
		self.timeline >> full

		self.actions_to_try = [
			evaluate_(),
			# swap_children_(),
			# add_(z),
			*[rule() for rule in SimplificationRule.__subclasses__()],
			AlgebraicAction((a/b)**n, (b/a)**-n, [[], '1-']),
			AlgebraicAction((sin**2)(t) + (cos**2)(t), 1, ['', '']),
			AlgebraicAction(Taylor(sin(t),t), sin(t), ['', '']),
			# replace_with_(x*t)
		]
		self.toggle_selection_mode()

		self.add(self.timeline.mob)
		self.embed()

	def get_highlight(self, mobject: Mobject) -> Mobject:
		return Mobject()
		if isinstance(mobject, VMobject) and mobject.has_points() and not self.select_top_level_mobs:
			length = max([mobject.get_height(), mobject.get_width()])
			result = VHighlight(
				mobject,
				max_stroke_addition=min([50 * length, 10]),
				n_layers=1
			)
			result.add_updater(lambda m: m.replace(mobject, stretch=True))
			return result
		elif isinstance(mobject, DotCloud):
			return Mobject()
		else:
			return self.get_corner_dots(mobject)
	
	def gather_new_selection(self):
		super().gather_new_selection()
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
		expression = expression or self.timeline.exp
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
	
	def view_ladder(self):
		self.save_state()
		self.clear()
		self.add(self.timeline.get_mob_ladder()),
	



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