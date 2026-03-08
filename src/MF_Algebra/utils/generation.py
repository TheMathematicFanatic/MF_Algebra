
def random_number_expression(leaves=range(-5, 10), max_depth=3, max_children_per_node=2, **kwargs):
	import random
	from ..expressions.numbers import Integer
	from ..expressions.combiners.operations import Add, Sub, Mul, Div, Pow, Negative
	nodes = [Add, Sub, Mul, Div, Pow]
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

