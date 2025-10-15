from .algebra_core import AlgebraicAction
from ..permutations import swap_children_
from ...expressions.variables import a,b,c
from MF_Tools.dual_compatibility import FadeIn, FadeOut, Write, PI


class EquationManeuver(AlgebraicAction):
	# Watch out, these cannot be preaddressed currently.
	# But I can't conceive of why you'd want to do that anyway.
	# Perhaps for a sequence of equations?
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def reverse(self):
		# swaps input and output templates
		self.template1, self.template2 = self.template2, self.template1
		# modifies addressmap accordingly
		# (swap order and negate path_arcs)
		for entry in self.addressmap:
			entry[0], entry[1] = entry[1], entry[0]
			if len(entry) == 3 and 'path_arc' in entry[2].keys():
				entry[2]['path_arc'] = -entry[2]['path_arc']
		return self

	def flip(self):
		# flips the equations of both templates
		s = swap_children_()
		self.template1 = s.get_output_expression(self.template1)
		self.template2 = s.get_output_expression(self.template2)
		# modifies addressmap accordingly
		# (swap first character of addresses and negate path_arcs)
		for entry in self.addressmap:
			if isinstance(entry[0], str):
				entry[0] = str(1-int(entry[0][0])) + entry[0][1:]
			if isinstance(entry[1], str):
				entry[1] = str(1-int(entry[1][0])) + entry[1][1:]
			if len(entry) == 3 and 'path_arc' in entry[2].keys():
				entry[2]['path_arc'] = -entry[2]['path_arc']
		return self

	def reverse_flip(self):
		return self.reverse().flip()



class alg_add_R(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a + b & c,
			a & c - b,
			**kwargs
		)
		self.addressmap = (
			['01', '11', {'path_arc':PI}],
			['0+', '1-', {'path_arc':PI}],
		)


class alg_add_L(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a + b & c,
			b & c - a,
			**kwargs
		)
		self.addressmap = (
			['00', '11', {'path_arc':PI}],
			['0+', '1-', {'path_arc':PI}]
		)
		# return (
		#     ['00', '11', {'path_arc':PI}],
		#     ['0+', FadeOut, {'run_time':0.5}],
		#     [FadeIn, '1-', {'run_time':0.5, 'delay':0.5}]
		# )


class alg_mul_R(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a * b & c,
			a & c / b,
			**kwargs
		)
		self.addressmap = (
			['01', '11', {'path_arc':PI}],
			['0*', FadeOut, {'run_time':0.5}],
			[Write, '1/', {'run_time':0.5, 'delay':0.5}]
		)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['11', '01', {'path_arc':-PI}],
			[Write, '0*', {'run_time':0.5, 'delay':0.5}],
			['1/', FadeOut, {'run_time':0.5}]
		)
		return self


class alg_mul_L(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a * b & c,
			b & c / a,
			**kwargs
		)
		self.addressmap = (
			['00', '11', {'path_arc':PI}],
			['0*', FadeOut, {'run_time':0.5}],
			[Write, '1/', {'run_time':0.5, 'delay':0.5}]
		)

	def reverse(self):
		super().reverse()
		self.addressmap = (
			['11', '00', {'path_arc':-PI}],
			[Write, '0*', {'run_time':0.5, 'delay':0.5}],
			['1/', FadeOut, {'run_time':0.5}]
		)
		return self


from ...expressions.functions.radicals import Rad
class alg_pow_R(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a**b & c,
			a & Rad(b)(c),
			**kwargs
		)
		self.addressmap = (
			['01', '100', {'path_arc':-PI/3}],
			[Write, '10f', {'delay':0.5, 'run_time':0.5}],
		)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['100', '01', {'path_arc':PI/3}],
			['10f', FadeOut, {'run_time':0.5}]
		)
		return self


from ...expressions.functions.logarithms import Log
class alg_pow_L(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			a**b & c,
			b & Log(a)(c),
			**kwargs
		)
		self.addressmap = (
			['00', '100', {'path_arc':PI/2}],
			[Write, '10f', {'delay':0.75, 'run_time':0.75}],
		)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['100', '00', {'path_arc':-PI/2}],
			['10f', FadeOut, {'run_time':0.5}]
		)
		return self



class alg_neg_R(EquationManeuver):
	def __init__(self, **kwargs):
		super().__init__(
			-a & b,
			a & -b,
			**kwargs
		)
		self.addressmap = (
			['0-', '1-', {'path_arc':PI}],
		)
