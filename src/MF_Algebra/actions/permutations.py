from .action_core import Action
from MF_Tools.dual_compatibility import PI, DEGREES


class Permutation:
	def __init__(self, *order):
		# Permutation(1,0,3,2)
		self.order = order

	def __len__(self):
		return len(self.order)

	def __call__(self, n):
		assert isinstance(n, int) and n >= 0
		if 0 <= n < len(self.order):
			return self.order[n]
		else:
			return n

	def __matmul__(self, other):
		assert isinstance(other, Permutation)
		N = max(len(self), len(other))
		return Permutation(*[self(other(n)) for n in range(N)])

	def inverse_call(self, n):
		if n in self.order:
			return self.order.index(n)
		else:
			return n

	def __invert__(self):
		return Permutation(*[self.inverse_call(n) for n in range(len(self))])

	@classmethod
	def from_cycles(cls, *cycles):
		order = []
		all_values_present = {n for cycle in cycles for n in cycle}
		max_val = max(all_values_present)
		for i in range(max_val+1):
			if i in all_values_present:
				for cycle in cycles:
					if i in cycle:
						index = cycle.index(i)
						index += 1
						value = cycle[index % len(cycle)]
						order.append(value)
						break
			else:
				order.append(i)
			i += 1
		return cls(*order)

	def __repr__(self):
		return 'Permutation' + str(self.order)



class permute_children_(Action):
	def __init__(self, permutation, mode='arc', arc_size=0.75*PI, **kwargs):
		self.permutation = permutation
		self.mode = mode
		self.arc_size = arc_size
		super().__init__(**kwargs)

	def get_output_expression(self, input_expression=None):
		input_expression.children = [
			input_expression.children[self.permutation(i)]
			for i in range(len(input_expression.children))
		]
		return input_expression

	def get_addressmap(self, input_expression=None):
		assert len(input_expression.children) >= len(self.permutation)
		
		if self.mode == 'arc':
			kwarg_dict = {'path_arc': self.arc_size}
		elif self.mode == 'straight':
			kwarg_dict == {}
		else:
			raise ValueError(f'Invalid mode: {self.mode}. Must be \'arc\' or \'straight\'.')
		
		addressmap = [
			[str(n), str(self.permutation(n)), kwarg_dict]
			for n in range(len(self.permutation))
		]

		from ..expressions.combiners import Combiner
		if isinstance(input_expression, Combiner):
			addressmap.append(['+', '+', kwarg_dict])

		return addressmap


# class swap_children_(permute_children_):
# 	def __init__(self, **kwargs):
# 		super().__init__(
# 			permutation = Permutation(1,0),
# 			**kwargs
# 		)


class swap_children_(Action):
	def __init__(self, arc_degrees=180, **kwargs):
		self.arc_degrees = arc_degrees
		super().__init__(**kwargs)
	
	def get_output_expression(self, input_expression):
		exp_type = type(input_expression)
		children = input_expression.children
		return exp_type(*children[::-1])
	
	def get_addressmap(self, input_expression):
		return [
			['0', '1', {'path_arc':self.arc_degrees*DEGREES}],
			['1', '0', {'path_arc':self.arc_degrees*DEGREES}],

		]

swap = swap_children_()