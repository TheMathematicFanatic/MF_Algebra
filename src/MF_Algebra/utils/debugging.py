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



def _tree_layout(addresses, x_spacing=0.5, y_spacing=1.0, node_widths=None): # AI written (Claude)
	"""
	Compute (x, y) coordinates for a tree whose nodes are identified by
	concatenated-digit-string addresses (e.g. '', '0', '1', '01', '10').

	Uses the Reingold-Tilford algorithm (Buchheim et al. linear-time variant)
	to produce a layout that is:
	- Downward-growing (y increases with depth)
	- Non-overlapping (no two nodes share a position)
	- Compact (siblings are packed as tightly as x_spacing allows)
	- Aesthetically balanced (parents centred over children; symmetric
		subtrees are mirror images of each other)

	Args:
		addresses   : list of address strings, e.g. ['', '0', '1', '00', '01']
		x_spacing   : minimum horizontal gap between node *edges* (default 1.0)
		y_spacing   : vertical distance between depth levels (default 1.0)
		node_widths : optional dict mapping address -> width (default 1.0 for all).
					The x coordinate returned for each node is its centre.
					Nodes with wider labels are spaced further from their
					siblings so that edges never overlap.

	Returns:
		dict mapping each address -> (x: float, y: float)
	"""
	import sys
	sys.setrecursionlimit(max(sys.getrecursionlimit(), len(addresses) * 10))

	addr_set = set(addresses)

	# ------------------------------------------------------------------ #
	# 0.  Node widths                                                    #
	# ------------------------------------------------------------------ #

	_nw = node_widths or {}
	nw = {a: _nw.get(a, 1.0) for a in addresses}   # width of each node

	def gap(u, v):
		"""Minimum centre-to-centre distance so u and v don't overlap."""
		return nw[u] / 2.0 + x_spacing + nw[v] / 2.0

	# ------------------------------------------------------------------ #
	# 1.  Build tree structure                                           #
	# ------------------------------------------------------------------ #

	def _children(addr):
		"""All addresses that are one digit longer and share the same prefix."""
		return sorted(
			[a for a in addr_set if len(a) == len(addr) + 1 and a.startswith(addr)],
			key=lambda a: a[-1],   # sort by the appended digit
		)

	children = {a: _children(a) for a in addresses}

	parent = {}
	for a in addresses:
		for child in children[a]:
			parent[child] = a

	roots = [a for a in addresses if a not in parent]
	if len(roots) != 1:
		raise ValueError(f"Expected exactly one root node, found: {roots}")
	root = roots[0]
	root_depth = len(root)   # usually 0 for root = ''

	# ------------------------------------------------------------------ #
	# 2.  Per-node mutable state                                         #
	# ------------------------------------------------------------------ #

	prelim   = {a: 0.0  for a in addresses}   # preliminary x
	mod      = {a: 0.0  for a in addresses}   # modifier passed down to subtree
	shift    = {a: 0.0  for a in addresses}   # accumulated shift (right)
	change   = {a: 0.0  for a in addresses}   # shift redistribution slope
	ancestor = {a: a    for a in addresses}   # used in contour comparison
	thread   = {a: None for a in addresses}   # cross-level pointer for contour walk

	# ------------------------------------------------------------------ #
	# 3.  Helper functions                                               #
	# ------------------------------------------------------------------ #

	def sibling_index(v):
		p = parent.get(v)
		return 0 if p is None else children[p].index(v)

	def left_sibling(v):
		p = parent.get(v)
		if p is None:
			return None
		siblings = children[p]
		idx = siblings.index(v)
		return siblings[idx - 1] if idx > 0 else None

	def leftmost_sibling(v):
		"""First child of v's parent (leftmost among v's siblings)."""
		p = parent.get(v)
		return None if p is None else children[p][0]

	def next_left(v):
		"""Step left along a contour: first child, or left thread."""
		ch = children[v]
		return ch[0] if ch else thread[v]

	def next_right(v):
		"""Step right along a contour: last child, or right thread."""
		ch = children[v]
		return ch[-1] if ch else thread[v]

	def get_ancestor(vim, v, default_ancestor):
		"""
		Return the ancestor of vim that is a sibling of v,
		falling back to default_ancestor.
		"""
		anc = ancestor[vim]
		p = parent.get(v)
		if p is not None and anc in children[p]:
			return anc
		return default_ancestor

	# ------------------------------------------------------------------ #
	# 4.  Core Reingold-Tilford routines                                 #
	# ------------------------------------------------------------------ #

	def move_subtree(wm, wp, s):
		"""
		Shift the subtree rooted at wp rightward by s, recording the shift
		so execute_shifts can distribute it evenly across the in-between siblings.
		"""
		n = sibling_index(wp) - sibling_index(wm)
		if n > 0:
			change[wp] -= s / n
			shift[wp]  += s
			change[wm] += s / n
		prelim[wp] += s
		mod[wp]    += s

	def execute_shifts(v):
		"""
		Sweep right-to-left over v's children, applying accumulated shifts.
		This distributes the shifts that move_subtree placed on the endpoints.
		"""
		s = c = 0.0
		for w in reversed(children[v]):
			prelim[w] += s
			mod[w]    += s
			c         += change[w]
			s         += shift[w] + c

	def apportion(v, default_ancestor):
		"""
		Compare the right contour of the left neighbour subtree with the
		left contour of the current subtree; shift v's subtree if they
		would overlap, and set cross-level threads to allow future contour
		walks to continue cheaply.
		"""
		w = left_sibling(v)
		if w is None:
			return default_ancestor

		# Four walkers:  inside / outside  ×  right subtree (v) / left subtree (w)
		vip = vop = v           # inner / outer pointer on right (current) subtree
		vim = w                 # inner pointer on left subtree (nearest left sibling)
		vom = leftmost_sibling(v)  # outer pointer on left subtree (leftmost sibling)

		sir = mod[vip]
		sor = mod[vop]
		sil = mod[vim]
		sol = mod[vom]

		while True:
			nr = next_right(vim)
			nl = next_left(vip)
			if nr is None or nl is None:
				break

			vim = nr
			vip = nl
			vom = next_left(vom)
			vop = next_right(vop)
			ancestor[vop] = v

			s = (prelim[vim] + sil + nw[vim] / 2.0) - (prelim[vip] + sir - nw[vip] / 2.0) + x_spacing
			if s > 0:
				move_subtree(get_ancestor(vim, v, default_ancestor), v, s)
				sir += s
				sor += s

			sil += mod[vim]
			sir += mod[vip]
			sol += mod[vom]
			sor += mod[vop]

		# Extend threads to bridge any remaining contour gap
		if next_right(vim) is not None and next_right(vop) is None:
			thread[vop]  = next_right(vim)
			mod[vop]    += sil - sor

		if next_left(vip) is not None and next_left(vom) is None:
			thread[vom]  = next_left(vip)
			mod[vom]    += sir - sol
			default_ancestor = v

		return default_ancestor

	def first_walk(v):
		"""
		Post-order pass: assign preliminary x positions bottom-up,
		packing siblings together and recording mod offsets for parents.
		"""
		ch = children[v]
		if not ch:
			# Leaf: place next to left sibling (or at 0)
			ls = left_sibling(v)
			if ls is not None:
				prelim[v] = prelim[ls] + gap(ls, v)
		else:
			default_ancestor = ch[0]
			for w_ in ch:
				first_walk(w_)
				default_ancestor = apportion(w_, default_ancestor)
			execute_shifts(v)
			mid = (prelim[ch[0]] + prelim[ch[-1]]) / 2.0
			ls = left_sibling(v)
			if ls is not None:
				prelim[v] = prelim[ls] + gap(ls, v)
				mod[v]    = prelim[v] - mid
			else:
				prelim[v] = mid

	def second_walk(v, m, depth):
		"""
		Pre-order pass: propagate mod offsets downward to compute final x,
		and assign y from depth.
		"""
		result[v] = (prelim[v] + m, depth * y_spacing)
		for w in children[v]:
			second_walk(w, m + mod[v], depth + 1)

	# ------------------------------------------------------------------ #
	# 5.  Run and return                                                 #
	# ------------------------------------------------------------------ #

	result = {}
	first_walk(root)
	second_walk(root, 0.0, 0)
	return result



def get_graph_mobject(expr, color='#FFFFFF', stroke_width=2, show_addresses=True):
	from MF_Tools.dual_compatibility import VDict, VGroup, dc_Tex, Circle, Line
	from MF_Tools.dual_compatibility import UP, DOWN, LEFT, RIGHT
	from MF_Tools import scale_to_fit_mobject

	addresses = expr.get_all_addresses()
	ad_coord_dict = _tree_layout(addresses)

	def get_symbol(expr):
		from ..expressions.numbers import Integer, Real
		from ..expressions.variables import Variable
		from ..expressions.combiners import Combiner, Mul, Div, Pow, UnaryOperation
		from ..expressions.functions import Function, ApplyFunction, Rad, Log
		type_to_symbolfunc_dict = {
			Integer: lambda expr: str(expr.value),
			Real: lambda expr: expr.symbol if expr.symbol else str(expr),
			Variable: lambda expr: expr.symbol,
			Mul: lambda expr: '\\times',
			Div: lambda expr: '/',
			Pow: lambda expr: '\\wedge',
			Rad: lambda expr: '\\sqrt{}',
			Log: lambda expr: '\\log',
			ApplyFunction: lambda expr: '\\circledast',
			UnaryOperation: lambda expr: expr.symbol,
			Function: lambda expr: expr.symbol,
			Combiner: lambda expr: expr.symbol,
		}
		for T, F in type_to_symbolfunc_dict.items():
			if isinstance(expr, T):
				return F(expr)
		return 'Error'
	
	def get_node(expr):
		tex = dc_Tex(get_symbol(expr))
		circle = Circle(stroke_color=color, stroke_width=stroke_width)
		scale_to_fit_mobject(tex, circle)
		tex.scale(0.8)
		return VGroup(circle, tex).scale(0.25)

	Nodes = VDict({
		ad : get_node(expr.get_subex(ad)).move_to(coord[0]*RIGHT + coord[1]*DOWN)
		for ad, coord in ad_coord_dict.items()
		})

	def get_edge(node1,node2):
		def closest_circle_points(c1, c2, r):
			dx, dy = c2[0] - c1[0], c2[1] - c1[1]
			import math
			dist = math.hypot(dx, dy)
			nx, ny = dx / dist, dy / dist
			return (c1[0] + nx * r, c1[1] + ny * r, 0), (c2[0] - nx * r, c2[1] - ny * r, 0)
		c1 = node1[0].get_center()
		c2 = node2[0].get_center()
		r = node1[0].get_width() / 2
		return Line(*closest_circle_points(c1,c2,r), stroke_color=color, stroke_width=stroke_width)
	
	Edges = VDict({
		ad : get_edge(Nodes[ad], Nodes[ad[:-1]])
		for ad in addresses
		if ad != ''
	})

	result = VGroup(Nodes, Edges)

	if show_addresses: # This has stopped working for some reason
		def get_address_label(address):
			from MF_Tools.dual_compatibility import ORANGE, Text
			label = Text(str(address)).set_color(ORANGE)
			node = Nodes[address]
			scale_to_fit_mobject(label, node, buff=0)
			label.scale(0.2).next_to(node, UP, buff=0.1)
			return label
		
		Addresses = VGroup(*[
			get_address_label(ad)
			for ad in addresses
			if ad != ''
		])
		
		result.add(Addresses)

	result.center()
	return result


def debug_expression(expr, scene):
	from MF_Tools.dual_compatibility import VGroup, DOWN, Write
	scene.clear()
	graph = get_graph_mobject(expr)
	VGroup(expr.mob, graph).arrange(DOWN,buff=1)
	scene.play(Write(expr.mob))
	scene.play(Write(graph))
	print_info(expr)



def get_mob_ladder(timeline):
	from MF_Tools.dual_compatibility import VGroup, ArcBetweenPoints, RIGHT, LEFT, Text, ORANGE, DOWN, np, PI
	from MF_Tools import scale_to_fit
	ladder = VGroup()
	mobs = timeline.get_vgroup().copy()
	ladder.expressions = mobs.arrange(DOWN, buff=1, aligned_edge=RIGHT)
	ladder.graphs = VGroup(*[
		scale_to_fit(
			get_graph_mobject(exp), len_y=mob.get_height(), buff=0
		).next_to(mob, LEFT, buff=1).scale(1.2)
		for exp, mob in zip(timeline.expressions, mobs)
	])
	ladder.arrows = VGroup(*[
		ArcBetweenPoints(
			np.array([mobs.get_edge_center(RIGHT)[0], m1.get_center()[1]-0.1, 0]),
			np.array([mobs.get_edge_center(RIGHT)[0], m2.get_center()[1]+0.1, 0]),
			angle = -3/4*PI
		).shift(0.5*RIGHT).set_stroke(width=2, opacity=0.5)
		for m1, m2 in zip(mobs[:-1], mobs[1:])
	])
	ladder.actions = VGroup(*[
		Text(repr(act)).scale(0.6).next_to(arrow, RIGHT, buff=0.25)
		for act, arrow in zip(timeline.actions, ladder.arrows)
	])
	ladder.addressmaps = VGroup(*[
		scale_to_fit(
			VGroup(*[
				Text(str(entry)).set_color(ORANGE)
				for entry in addressmap
			]).arrange(DOWN),
			len_y = (
				ladder.actions[i].get_center()[1] - ladder.actions[i+1].get_center()[1]
				if i + 1 < len(ladder.actions)
				else ladder.actions[i-1].get_center()[1] - ladder.actions[i].get_center()[1]
			)*0.8,
			buff=0
		).next_to(ladder.actions[i], DOWN)
		for i, addressmap in enumerate([
			act.get_addressmap(exp)
			for exp, act in zip(timeline.expressions[:-1], timeline.actions)
		])
	])


	ladder.add(ladder.graphs, ladder.expressions, ladder.arrows, ladder.actions, ladder.addressmaps)
	return ladder