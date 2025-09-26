from .action_core import Action
from MF_Tools.dual_compatibility import PI


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




class permute_children_(Action):
	def __init__(self, permutation=Permutation(1,0), mode='arc', arc_size=0.75*PI, **kwargs):
		self.permutation = permutation
		self.mode = mode
		self.arc_size = arc_size
		super().__init__(**kwargs)

	@Action.preaddressfunc
	def get_output_expression(self, input_expression=None):
		input_expression.children = [
			input_expression.children[self.permutation(i)]
			for i in range(input_expression.children)
		]
		return input_expression

	@Action.autoparenmap
	@Action.preaddressmap
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



class swap_children_(permute_children_):
	def __init__(self, **kwargs):
		super().__init__(
			permutation = Permutation(1,0),
			**kwargs
		)
