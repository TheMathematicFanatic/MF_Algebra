import numpy as numpy
from .type_fixing import Smarten

def random_number_expression(leaves=range(-5, 10), max_depth=3, max_children_per_node=2, seed=None, **kwargs):
	import random
	from ..expressions.numbers import Integer
	from ..expressions.combiners.operations import Add, Sub, Mul, Div, Pow, Negative
	nodes = [Add, Sub, Mul, Div, Pow]
	random.seed(seed)
	node = random.choice(nodes)
	def generate_child(current_depth):
		if np.random.random() < 1 / (current_depth + 1):
			return Integer(random.choice(leaves))
		else:
			return random_number_expression(leaves, max_depth - 1)
	def generate_children(current_depth, number_of_children):
		return [generate_child(current_depth) for _ in range(number_of_children)]
	if node == Add or node == Mul:
		children = generate_children(max_depth, random.choice(list(range(2,max_children_per_node+1))))
	elif node == Negative:
		children = generate_children(max_depth, 1)
	else:
		children = generate_children(max_depth, 2)
	return node(*children, **kwargs)


def random_expression(
	leaves = [],
	leaf_weights = None,
	nodes = [],
	node_weights = None,
	max_depth = 3,
	min_depth = 2,
	seed = None,
	default_number_of_children_per_node = 2,
	**kwargs
):
	import random
	random.seed(seed)
	if random.random() < 1/max_depth and max_depth < min_depth:
		# leaf case
		leaf = random.choices(leaves, weights=leaf_weights)[0]
		return Smarten(leaf)
	else:
		# node case
		node = random.choices(nodes, weights=node_weights)[0]
		from ..expressions.combiners.operations import Operation, UnaryOperation, BinaryOperation
		assert issubclass(node, Operation)
		if issubclass(node, UnaryOperation):
			k = 1
		elif issubclass(node, BinaryOperation):
			k = 2
		else:
			k = default_number_of_children_per_node
		children = [
			random_expression(
				leaves = leaves,
				leaf_weights = leaf_weights,
				nodes = nodes,
				node_weights = node_weights,
				max_depth = max_depth - 1,
				min_depth = min_depth,
				seed = seed,
				default_number_of_children_per_node = default_number_of_children_per_node,
				**kwargs
			)
			for _ in range(k)
		]
		return node(*children)



def random_bool_exp(mode='simple', **kwargs):
	from ..logic import T,F,Not,And,Or,BooleanOperation
	if mode == 'simple':
		leaves = [T,F],
		nodes = [Not, And, Or]
	elif mode == 'full':
		leaves = [T,F]
		nodes = BooleanOperation.__subclasses__()
	else:
		raise ValueError('Invalid mode')
	return random_expression(
		leaves = leaves,
		nodes = nodes,
		**kwargs
	)
