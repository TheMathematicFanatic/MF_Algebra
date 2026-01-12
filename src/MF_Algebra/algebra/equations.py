from .algebra_core import AlgebraicAction
from ..actions.permutations import swap_children_
from ..expressions.variables import a,b,c
from ..expressions.functions.radicals import Rad, sqrt
from ..expressions.functions.logarithms import Log, ln
from ..expressions.numbers.real import e
from ..expressions.combiners.operations import PlusMinus
from MF_Tools.dual_compatibility import FadeIn, FadeOut, Write, PI
from copy import deepcopy


class EquationManeuver(AlgebraicAction):
	# Watch out, I don't think these cannot be preaddressed currently.
	# But I can't conceive of why you'd want to do that anyway.
	# Perhaps for a sequence of equations?

	def reverse(self):
		# swaps input and output templates
		self.template1, self.template2 = self.template2, self.template1
		# modifies addressmap accordingly
		# (swap order and negate path_arcs)
		admap_copy = deepcopy(self.addressmap)
		for entry in admap_copy:
			entry[0], entry[1] = entry[1], entry[0]
			if len(entry) == 3 and 'path_arc' in entry[2].keys():
				entry[2]['path_arc'] = -entry[2]['path_arc']
		self.addressmap = admap_copy

		return self

	def flip(self):
		# flips the equations of both templates
		s = swap_children_()
		self.template1 = s.get_output_expression(self.template1)
		self.template2 = s.get_output_expression(self.template2)
		# modifies addressmap accordingly
		# (swap first character of addresses and negate path_arcs)
		admap_copy = deepcopy(self.addressmap)
		for entry in admap_copy:
			if isinstance(entry[0], str):
				entry[0] = str(1-int(entry[0][0])) + entry[0][1:]
			if isinstance(entry[1], str):
				entry[1] = str(1-int(entry[1][0])) + entry[1][1:]
			if len(entry) == 3 and 'path_arc' in entry[2].keys():
				entry[2]['path_arc'] = -entry[2]['path_arc']
		self.addressmap = admap_copy

		return self

	def reverse_flip(self):
		return self.reverse().flip()


class alg_add_R(EquationManeuver):
	template1 = a + b | c
	template2 = a | c - b
	addressmap = (
		['01', '11', {'path_arc':PI}],
		['0+', '1-', {'path_arc':PI}],
	)


class alg_add_L(EquationManeuver):
		template1 = a + b | c
		template2 = b | c - a
		addressmap = (
			['00', '11', {'path_arc':PI}],
			['0+', '1-', {'path_arc':PI}]
		)
		# return (
		#     ['00', '11', {'path_arc':PI}],
		#     ['0+', FadeOut, {'run_time':0.5}],
		#     [FadeIn, '1-', {'run_time':0.5, 'delay':0.5}]
		# )


class alg_mul_R(EquationManeuver):
	template1 =	a * b | c
	template2 = a | c / b
	addressmap = (
		['01', '11', {'path_arc':PI}],
		['0*', [], {'run_time':0.5}],
		[[], '1/', {'run_time':0.5, 'delay':0.5}]
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
	template1 = a * b | c
	template2 = b | c / a
	addressmap = (
		['00', '11', {'path_arc':PI}],
		['0*', [], {'run_time':0.5}],
		[[], '1/', {'run_time':0.5, 'delay':0.5}]
	)

	def reverse(self):
		super().reverse()
		self.addressmap = (
			['11', '00', {'path_arc':-PI}],
			[Write, '0*', {'run_time':0.5, 'delay':0.5}],
			['1/', FadeOut, {'run_time':0.5}]
		)
		return self


class alg_pow_2_R(EquationManeuver):
	template1 = a**2 | b
	template2 = a | PlusMinus(sqrt(b))
	addressmap = (
		['01', '10f', {'path_arc':-PI/3}],
		[[], '1~']
	)
	
	def reverse(self): # Hopefully this never happens lol
		super().reverse()
		self.addressmap = (
			['10f', '01', {'path_arc':PI/3}],
		)
		return self


class alg_pow_R(EquationManeuver):
	template1 = a**b | c
	template2 = a | Rad(b)(c)
	addressmap = (
		['01', '100', {'path_arc':-PI/3}],
		[[], '10f', {'delay':0.5, 'run_time':0.5}],
	)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['100', '01', {'path_arc':PI/3}],
			['10f', [], {'run_time':0.5}]
		)
		return self


class alg_pow_e_L(EquationManeuver):
	template1 = e**a | b
	template2 = a | ln(b)
	addressmap = (
		['00', '10f', {'path_arc':PI/2}],
	)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['10f', '00', {'path_arc':-PI/2}],
		)
		return self


class alg_pow_L(EquationManeuver):
	template1 = a**b | c
	template2 = b | Log(a)(c)
	addressmap = (
		['00', '100', {'path_arc':PI/2}],
		[[], '10f', {'delay':0.75, 'run_time':0.75}],
	)
	
	def reverse(self):
		super().reverse()
		self.addressmap = (
			['100', '00', {'path_arc':-PI/2}],
			['10f', FadeOut, {'run_time':0.5}]
		)
		return self


class alg_neg_R(EquationManeuver):
	template1 = -a | b
	template2 = a | -b
	addressmap = (
		['0-', '1-', {'path_arc':PI}],
	)
