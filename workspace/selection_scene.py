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


		self.timeline = Timeline()
		self.timeline >> full
		self.add(self.timeline.mob)
		self.embed()
	




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

	def apply_action_at_selection(self, action):
		self.clear_selection()
		address = self.get_address_from_selection()
		self.apply_action_at_address(action, address)
	
	def ready_action(self, action):
		while not self.selection:
			pass
		self.apply_action_at_selection(action)



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


class rewrap_subex_(AlgebraicAction):
	def __init__(self,
		start_exp:Expression,
		end_exp:Expression,
		target_subex:Expression,
		**kwargs
	):
		self.target_subex = target_subex
		self.start_exp = start_exp
		self.end_exp = end_exp
		start_ads = start_exp.get_addresses_of_subex(target_subex)
		end_ads = end_exp.get_addresses_of_subex(target_subex)
		assert len(start_ads) == len(end_ads) == 1, 'Target subexpression must be unique in both expressions.'
		# I'd love to make it work for several but I don't know how to get all glyphs except for more than one subexpression in an addressmap
		self.start_ad = start_ads[0]
		self.end_ad = end_ads[0]
		super().__init__(self.start_exp, self.end_exp, **kwargs)
	
	def get_addressmap(self, input_expression=None):
		return [
			[self.start_ad, self.end_ad, {'delay':0.25}],
			['!'+self.start_ad, '!'+self.end_ad, {'path_arc':PI}],
		]


rw = rewrap_subex_(
	Sum(n,0,inf)(x**n),
	1/(1-x),
	x
)

pyth = (sin**2)(t) + (cos**2)(t)

class unwrap_subex_(rewrap_subex_):
	def __init__(self, outer_exp, target_subex, **kwargs):
		super().__init__(outer_exp, target_subex, target_subex, **kwargs)


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
		print('zoom_decorator')
		def decorator(func):
			print('decorator')
			def wrapper(self, *args, **kwargs):
				print('wrapper')
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
		print('trig_frac')
		self.timeline >> AlgebraicAction(e**ln(a), a).pread('1101') >> substitute_({pyth:1}) >> evaluate_()
	

	def denom_base(self):
		pass


	def upper(self):
		address1 = self.timeline.exp.get_addresses_of_subex(upper)[0]
		self.zoom_to_selected(address1)
		address2 = self.timeline.exp.get_addresses_of_subex(upper_series)[0]
		self.zoom_to_selected(address2)
		self.timeline >> substitute_({sin(pi/6):1/two}) >> rw >> evaluate_()
		self.restore_to_original()
		self.timeline >> unwrap_subex_(self.timeline.exp, inf)
		self.restore_to_original()



