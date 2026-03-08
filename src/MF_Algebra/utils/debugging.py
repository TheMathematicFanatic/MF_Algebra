from tabulate import tabulate


def print_info(expression, tablefmt='rst'):
	def tree_prefix(address):
		V, T = '│ ', '├─'
		d = len(address)
		return (V * (d - 1) + T) if d else ''

	def get_all_info(expression, address):
		def get_info(callable):
			try:
				result = callable(expression, address)
				string = str(result)
			except Exception as e:
				string = str(e)
			max_length = 20
			if len(string) > max_length:
				string = string[:max_length-3] + '...'
			return string

		return {
			'Type': get_info(lambda Exp, ad: f'{tree_prefix(ad)}{type(Exp.get_subex(ad)).__name__}'),
			'Address': get_info(lambda Exp, ad: ad),
			'LaTeX string': get_info(lambda Exp, ad: str(Exp.get_subex(ad))),
			'glyph_count': get_info(lambda Exp, ad: str(Exp.get_subex(ad).glyph_count)),
			'glyph_indices': get_info(lambda Exp, ad: Exp.get_glyphs_at_address(ad)),
			'paren': get_info(lambda Exp, ad: Exp.get_subex(ad).parentheses),
			'color': get_info(lambda Exp, ad: getattr(Exp.get_subex(ad), 'color', None))
		}

	addresses = expression.get_all_addresses()
	rows = [get_all_info(expression, address) for address in addresses]
	table = tabulate(
		rows,
		headers='keys',
		tablefmt=tablefmt
	)
	print(table)


# def create_graph(expr, node_size=0.5, horizontal_buff=1, vertical_buff=1.5, printing=False):
# 	def create_node(address):
# 		from .expressions.numbers import Integer, Real, Rational
# 		from .expressions.variables import Variable
# 		from .expressions.combiners.operations import Add, Sub, Mul, Div, Pow, Negative
# 		from .expressions.functions.functions import Function
# 		from .expressions.combiners.sequences import Sequence
# 		from .expressions.combiners.relations import Equation, LessThan, LessThanOrEqualTo, GreaterThan, GreaterThanOrEqualTo
# 		type_to_symbol_dict = {
# 			Integer: lambda expr: str(expr.value),
# 			Real: lambda expr: expr.symbol if expr.symbol else str(expr),
# 			Rational: lambda expr: '\\div',
# 			Variable: lambda expr: expr.symbol,
# 			Add: lambda expr: '+',
# 			Sub: lambda expr: '-',
# 			Mul: lambda expr: '\\times',
# 			Div: lambda expr: '\\div',
# 			Pow: lambda expr: '\\hat{}',
# 			Negative: lambda expr: '-',
# 			Function: lambda expr: expr.symbol,
# 			Sequence: lambda expr: ',',
# 			Equation: lambda expr: '=',
# 			LessThan: lambda expr: '<',
# 			LessThanOrEqualTo: lambda expr: '\\leq',
# 			GreaterThan: lambda expr: '>',
# 			GreaterThanOrEqualTo: lambda expr: '\\geq',
# 		}
# 		subex = expr.get_subex(address)
# 		symbol = type_to_symbol_dict[type(subex)](subex)
# 		tex = Tex(symbol)
# 		# if tex.width > tex.height:
# 		# 	tex.scale_to_fit_width(node_size)
# 		# else:
# 		# 	tex.scale_to_fit_height(node_size)
# 		return tex
# 	addresses = expr.get_all_addresses()
# 	if printing: print(addresses)
# 	max_length = max(len(address) for address in addresses)
# 	layered_addresses = [
# 		[ad for ad in addresses if len(ad) == i]
# 		for i in range(max_length + 1)
# 	]
# 	if printing: print(layered_addresses)
# 	max_index = max(range(len(layered_addresses)), key=lambda i: len(layered_addresses[i]))
# 	max_layer = layered_addresses[max_index]
# 	max_width = len(max_layer)
# 	if printing: print(max_index, max_width, max_layer)
# 	Nodes = VDict({ad: create_node(ad) for ad in addresses})
# 	#Max_layer = VGroup(*[Nodes[ad] for ad in max_layer]).arrange(RIGHT,buff=horizontal_buff)
# 	def position_children(parent_address):
# 		parent = Nodes[parent_address]
# 		child_addresses = [ad for ad in layered_addresses[len(parent_address)+1] if ad[:-1] == parent_address]
# 		if printing: print(child_addresses)
# 		child_Nodes = VGroup(*[Nodes[ad] for ad in child_addresses]).arrange(RIGHT,buff=1)
# 		child_Nodes.move_to(parent.get_center()+DOWN*vertical_buff)
# 	for i in range(max_index, max_length):
# 		for ad in layered_addresses[i]:
# 			position_children(ad)
# 	def position_parent(child_address):
# 		sibling_Nodes = VGroup(*[Nodes[ad] for ad in layered_addresses[len(child_address)] if ad[:-1] == child_address[:-1]])
# 		parent_Node = Nodes[child_address[:-1]]
# 		parent_Node.move_to(sibling_Nodes.get_center()+UP*vertical_buff)
# 	for i in range(max_index, 0, -1):
# 		for ad in layered_addresses[i]:
# 			position_parent(ad)
# 	Edges = VGroup(*[
# 		Line(
# 			Nodes[ad[:-1]].get_bounding_box_point(DOWN),
# 			Nodes[ad].get_bounding_box_point(UP),
# 			buff=0.2, stroke_opacity=0.4
# 			)
# 		for ad in addresses if len(ad) > 0
# 		])
# 	return VGroup(Nodes, Edges)

