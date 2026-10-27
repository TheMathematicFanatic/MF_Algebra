from ..actions.action_core import Action, IncompatibleExpression
from ..expressions.expression_core import Address
from ..expressions.combiners.operations import Add, Sub, Mul, Div, Pow
from ..logic.operations import And, Or, Implies, Xor
from ..sets.operations import Union, Intersection, Difference, CartesianProduct
from ..utils import merge_dicts, merge_lists
from typing import Literal


both_distribute_table = {
	Mul: (Add, Sub),
	And: (Or, Xor),
	Or: (And,),
	Intersection: (Union, Difference),
	Union: (Intersection,),
	CartesianProduct: (Union, Intersection, Difference)
}

left_distribute_table = {
	Implies: (And, Or)
}

right_distribute_table = {
	Div: (Add, Sub),
	Pow: (Mul, Div),
}



class distribute_(Action):
	def __init__(self, mode: Literal['auto', 'left', 'right'] = 'auto', **kwargs):
		self.mode = mode
		super().__init__(**kwargs)
	
	def determine_mode(self, input_expression):
		input_expression = input_expression.get_subex(self.preaddress)
		Outer = type(input_expression)
		distribute_table = merge_dicts(both_distribute_table, left_distribute_table)
		if Outer in distribute_table:
			Inner = type(input_expression.children[1])
			if Inner in distribute_table[Outer]:
				self.mode = 'left'
				return self.mode, Outer, Inner
		distribute_table = merge_dicts(both_distribute_table, right_distribute_table)
		if Outer in distribute_table:
			Inner = type(input_expression.children[0])
			if Inner in distribute_table[Outer]:
				self.mode = 'right'
				return self.mode, Outer, Inner
		raise IncompatibleExpression(f'Cannot distribute {input_expression}')

	def get_output_expression(self, input_expression=None):
		self.mode, Outer, Inner = self.determine_mode(input_expression)
		try:
			if self.mode == 'left':
				return Inner(*[Outer(input_expression.children[0],child) for child in input_expression.children[1].children])
			if self.mode == 'right':
				return Inner(*[Outer(child, input_expression.children[1]) for child in input_expression.children[0].children])
		except:
			pass
		raise IncompatibleExpression(f'Cannot distribute {input_expression}')
	
	def get_addressmap(self, input_expression=None):
		self.mode, Outer, Inner = self.determine_mode(input_expression)
		if self.mode == 'left':
			num_children = len(input_expression.children[1].children)
			return merge_lists(
				[['0', Address(i)+'0', {'path_arc':-3}] for i in range(num_children)],
				[['1+', '+']],
				[['*', Address(i)+'*'] for i in range(num_children)]
			)
		elif self.mode == 'right':
			num_children = len(input_expression.children[0].children)
			return merge_lists(
				[['1', Address(i)+'1'] for i in range(num_children)],
				[['0+', '+']],
				[['*', Address(i)+'*', {'run_time':0.75}] for i in range(num_children)]
			)
		else:
			raise ValueError(f"Invalid mode: {self.mode}")
	
	def get_trigger_addresses(self):
		if self.mode == 'left':
			return ['*0']
		elif self.mode == 'right':
			return ['*1']



