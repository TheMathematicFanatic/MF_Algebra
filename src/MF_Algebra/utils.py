from MF_Tools.dual_compatibility import (
	Text, dc_Tex as Tex,
	UP, DOWN, LEFT, RIGHT,
	GREEN, BLUE, ORANGE,
	Indicate,
	VGroup, VDict,
	Line,
	Scene
)
import numpy as np
from abc import ABC
from dataclasses import dataclass
from copy import deepcopy
from tabulate import tabulate



@dataclass
class MF_Base(ABC):
	def copy(self):
		return deepcopy(self)

	def __rshift__(self, other):
		other = Smarten(other)
		return combine_to_timeline(self, other)

	def __rrshift__(self, other):
		other = Smarten(other)
		return other.__rshift__(self)

	def __eq__(self, other):
		other = Smarten(other)
		if type(self) != type(other):
			return False
		else:
			return self.hash_key() == other.hash_key()

	def __hash__(self):
		return hash(self.hash_key())

	def hash_key(self):
		raise NotImplementedError


def Smarten(input):
	if input is None:
		return None

	if isinstance(input, MF_Base):
		return input.copy()

	if isinstance(input, int):
		from .expressions.numbers.integer import Integer
		return Integer(input)

	if isinstance(input, float):
		if input == np.inf:
			from .calculus.limits import inf
			return inf
		if input == np.nan:
			return None
		from math import isclose
		if isclose(input, round(input)):
			from .expressions.numbers.integer import Integer
			return Integer(int(input))
		from .expressions.numbers.real import Real
		return Real(input)

	if isinstance(input, complex):
		from .expressions.numbers.complex import Complex
		return Complex(input)

	if input is ...:
		from .expressions.variables import dots
		return dots

	from decimal import Decimal
	if isinstance(input, Decimal):
		return Smarten(float(input))

	from fractions import Fraction
	if isinstance(input, Fraction):
		from .expressions.numbers.rational import Rational
		return Rational(input.numerator, input.denominator)

	raise NotImplementedError(f"Unsupported type {type(input)}")


def combine_to_timeline(A, B):
	from .expressions.expression_core import Expression
	from .actions.action_core import Action
	from .timelines.timeline_core import Timeline
	type_combo_to_timeline_func = {
		# (TypeofA, TypeofB) : function of A,B which returns the desired Timeline object
		(Expression, Expression) : lambda A,B: Timeline().add_expression_to_start(A).add_expression_to_end(B),
		(Expression, Action) : lambda A,B: Timeline().add_expression_to_start(A).add_action_to_end(B),
		(Action, Expression) : lambda A,B: Timeline().add_action_to_start(A).add_expression_to_end(B),
		(Action, Action) : lambda A,B: Timeline().add_action_to_start(A).add_action_to_end(B),
		(Expression, Timeline) : lambda A,B: B.add_expression_to_start(A),
		(Action, Timeline) : lambda A,B: B.add_action_to_start(A),
		(Timeline, Expression) : lambda A,B: A.add_expression_to_end(B),
		(Timeline, Action) : lambda A,B: A.add_action_to_end(B),
		(Timeline, Timeline) : lambda A,B: A.combine_timelines(B)
	}
	for (type1, type2), func in type_combo_to_timeline_func.items():
		if isinstance(A, type1) and isinstance(B, type2):
			return func(A, B)
	raise NotImplementedError(f"Unsupported combination of types {type(A)} and {type(B)}")


def add_spaces_around_brackets(input_string): #GPT
	result = []
	i = 0
	length = len(input_string)

	while i < length:
		if input_string[i] == '{' or input_string[i] == '}':
			if i > 0 and input_string[i - 1] != ' ':
				result.append(' ')
			result.append(input_string[i])
			if i < length - 1 and input_string[i + 1] != ' ':
				result.append(' ')
		else:
			result.append(input_string[i])
		i += 1

	# Join the list into a single string and remove any extra spaces
	spaced_string = ''.join(result).split()
	return ' '.join(spaced_string)


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


def random_number_expression(leaves=range(-5, 10), max_depth=3, max_children_per_node=2, **kwargs):
	import random
	from .expressions.numbers.number import Integer
	from .expressions.combiners.operations import Add, Sub, Mul, Div, Pow, Negative
	nodes = [Add, Sub, Mul, Pow]
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


def create_graph(expr, node_size=0.5, horizontal_buff=1, vertical_buff=1.5, printing=False):
	def create_node(address):
		from .expressions.numbers.number import Integer, Real, Rational
		from .expressions.variables import Variable
		from .expressions.combiners.operations import Add, Sub, Mul, Div, Pow, Negative
		from .expressions.functions.functions import Function
		from .expressions.combiners.sequences import Sequence
		from .expressions.combiners.relations import Equation, LessThan, LessThanOrEqualTo, GreaterThan, GreaterThanOrEqualTo
		type_to_symbol_dict = {
			Integer: lambda expr: str(expr.n),
			Real: lambda expr: expr.symbol if expr.symbol else str(expr),
			Rational: lambda expr: '\\div',
			Variable: lambda expr: expr.symbol,
			Add: lambda expr: '+',
			Sub: lambda expr: '-',
			Mul: lambda expr: '\\times',
			Div: lambda expr: '\\div',
			Pow: lambda expr: '\\hat{}',
			Negative: lambda expr: '-',
			Function: lambda expr: expr.symbol,
			Sequence: lambda expr: ',',
			Equation: lambda expr: '=',
			LessThan: lambda expr: '<',
			LessThanOrEqualTo: lambda expr: '\\leq',
			GreaterThan: lambda expr: '>',
			GreaterThanOrEqualTo: lambda expr: '\\geq',
		}
		subex = expr.get_subex(address)
		symbol = type_to_symbol_dict[type(subex)](subex)
		tex = Tex(symbol)
		# if tex.width > tex.height:
		# 	tex.scale_to_fit_width(node_size)
		# else:
		# 	tex.scale_to_fit_height(node_size)
		return tex
	addresses = expr.get_all_addresses()
	if printing: print(addresses)
	max_length = max(len(address) for address in addresses)
	layered_addresses = [
		[ad for ad in addresses if len(ad) == i]
		for i in range(max_length + 1)
	]
	if printing: print(layered_addresses)
	max_index = max(range(len(layered_addresses)), key=lambda i: len(layered_addresses[i]))
	max_layer = layered_addresses[max_index]
	max_width = len(max_layer)
	if printing: print(max_index, max_width, max_layer)
	Nodes = VDict({ad: create_node(ad) for ad in addresses})
	#Max_layer = VGroup(*[Nodes[ad] for ad in max_layer]).arrange(RIGHT,buff=horizontal_buff)
	def position_children(parent_address):
		parent = Nodes[parent_address]
		child_addresses = [ad for ad in layered_addresses[len(parent_address)+1] if ad[:-1] == parent_address]
		if printing: print(child_addresses)
		child_Nodes = VGroup(*[Nodes[ad] for ad in child_addresses]).arrange(RIGHT,buff=1)
		child_Nodes.move_to(parent.get_center()+DOWN*vertical_buff)
	for i in range(max_index, max_length):
		for ad in layered_addresses[i]:
			position_children(ad)
	def position_parent(child_address):
		sibling_Nodes = VGroup(*[Nodes[ad] for ad in layered_addresses[len(child_address)] if ad[:-1] == child_address[:-1]])
		parent_Node = Nodes[child_address[:-1]]
		parent_Node.move_to(sibling_Nodes.get_center()+UP*vertical_buff)
	for i in range(max_index, 0, -1):
		for ad in layered_addresses[i]:
			position_parent(ad)
	Edges = VGroup(*[
		Line(
			Nodes[ad[:-1]].get_bounding_box_point(DOWN),
			Nodes[ad].get_bounding_box_point(UP),
			buff=0.2, stroke_opacity=0.4
			)
		for ad in addresses if len(ad) > 0
		])
	return VGroup(Nodes, Edges)


def to_sympy(exp):
	from sympy.parsing.latex import parse_latex
	latex = str(exp)
	sympy_expr = parse_latex(latex)

	# Special case substitution needed so that e is interpreted as the constant and not a variable
	from sympy import E, symbols
	sympy_expr = sympy_expr.subs(symbols('e'), E)

	return sympy_expr


def from_MathJSON(json):
	from .expressions import (
		Add, Sub, Mul, Div, Pow,
		Integer, Real, Variable
	)
	if isinstance(json, dict):
		json = json["fn"]
	if isinstance(json, int):
		return Integer(json)
	if isinstance(json, float):
		return Real(json)
	if isinstance(json, str):
		return Variable
	if isinstance(json, (list, tuple)):
		json = list(json)
		top_level = json[0]
		top_string_to_MF_class_dict = {
			"Add" : Add,
			"Subtract" : Sub,
		}



def text_to_MF_Algebra(text):
	import re
	# Token regex
	token_re = re.compile(
		r"""
		(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)   # numbers
		| [a-zA-Z_]\w*                     # identifiers
		| \^                                # caret
		| =                                 # equals
		| [()+\-*/]                         # operators and parentheses
		""",
		re.VERBOSE
	)

	# Helper to categorize tokens
	def categorize(tok):
		if tok in '+-*/()|**':
			return 'op'
		if tok == '**':
			return 'caret'
		if tok == '|':
			return 'equals'
		if re.match(r'(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)$', tok):
			return 'number'
		return 'identifier'

	def rewrite_expression(s):
		# Step 1: tokenize & replace numbers/operators
		raw_tokens = token_re.findall(s)
		tokens = []
		for tok in raw_tokens:
			if tok == '^':
				tokens.append('**')
			elif tok == '=':
				tokens.append('|')
			elif re.match(r'(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)$', tok):
				tokens.append(f"Real({tok})" if '.' in tok else f"Integer({tok})")
			else:
				tokens.append(tok)

		# Step 2: insert implicit multiplication
		result = [tokens[0]]
		for prev, curr in zip(tokens, tokens[1:]):
			prev_cat = categorize(prev)
			curr_cat = categorize(curr)
			
			# new rules for implicit multiplication
			if ((prev_cat in ('number', 'identifier') or prev == ')') and
				(curr_cat in ('number', 'identifier') or curr == '(')):
				result.append('*')
			result.append(curr)
		return ''.join(result)

	from asteval import Interpreter
	from MF_Algebra import (Integer, Real, Variable, Function, sqrt, cbrt)
	symtable = {
		**{L: Variable(L, 1) for L in 'abcjklmnopqrstuvwxyz'},
		**{F: Function(F, 1) for F in 'fgh'},
		'Integer' : Integer,
		'Real' : Real,
		'Variable' : Variable,
		'sqrt' : sqrt,
		'cbrt' : cbrt,
	}
	aeval = Interpreter(symtable=symtable)

	return aeval(rewrite_expression(text))





import dill as pickle
import os

def save_to_file(obj:MF_Base, filename:str) -> None:
	os.makedirs('saved_objects', exist_ok=True)
	path = os.path.join('saved_objects', filename)
	with open(path, 'wb') as f:
		pickle.dump(obj, f)

def load_from_file(filename:str) -> MF_Base:
	path = os.path.join('saved_objects', filename)
	with open(path, 'rb') as f:
		return pickle.load(f)




def apply_addressmap(address:str, addressmap:list, reverse:bool=False) -> set:
	"""    
	Turns one address into another (or several), according to an addressmap.
	If it is explicitly listed in the addressmap, it simply returns the address on the other side.
	If it is not listed, it checks all the entries with that address as a prefix, and outputs the corresponding prefix on the other side.
	It also checks if any entry is a prefix of the address, in which cases it replaces that section of the address with the corresponding prefix.
	It may be found multiple times or not at all, which is why it returns a set. I think that makes sense but I'm not sure.
	The output set can have any number, you usually are expecting a singleton, empty or multiple usually means failure.
	Reverse simply goes from right to left across the addressmap instead of left to right.
	Returns None if address is ever mapped to [], meaning that subex is meant to fade in or out.
	
	Examples:
	>>> apply_addressmap('12', [['123', '999']])
	{'99'}
	>>> apply_addressmap('123', [['12', '88'], ['1', '5']])
	{'883', '523'}
	>>> apply_addressmap('12', [['1', []]])
	None
	"""

	la = len(address)
	from_ads = [entry[int(reverse)] for entry in addressmap]
	to_ads = [entry[int(not reverse)] for entry in addressmap]
	results = set()

	for from_ad, to_ad in zip(from_ads, to_ads):
		if isinstance(from_ad, type) or isinstance(to_ad, type):
			# Address is being explicitly animated in or out
			return None

		lf,lt = len(from_ad), len(to_ad)

		# Case 1: address is equal to from_ad or some prefix of it
		if address == from_ad[:la]:
			if to_ad == []: return None
			results.add(to_ad[:la-lf or None])

		# Case 2: from_ad is a prefix of address
		elif from_ad == address[:lf]:
			if to_ad == []: return None
			results.add(to_ad + address[lf:])

	return results