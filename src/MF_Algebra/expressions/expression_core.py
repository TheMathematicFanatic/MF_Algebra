# expressions.py
from MF_Tools.dual_compatibility import dc_Tex as Tex, MANIM_TYPE, VGroup
from ..utils import Smarten, add_spaces_around_brackets
from copy import deepcopy
import numpy as np


algebra_config = {
		"auto_parentheses": True,
		"multiplication_mode": "auto",
		"division_mode": "fraction",
		"decimal_precision": 4,
		"always_color": {},
		"fast_paren_length": True
	}

class Expression:
	def __init__(self, children=[], parentheses=False, **kwargs):
		self.children = list(map(Smarten,children))
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		self._mob = None
		self._number_of_glyphs = None


	### Mobject ###

	@property
	def mob(self):
		if self._mob is None:
			self.init_mob()
		return self._mob

	def init_mob(self, **kwargs):
		string = add_spaces_around_brackets(str(self))
		self._mob = Tex(string, **kwargs)
		self.set_color_by_subex(algebra_config["always_color"])

	def __getitem__(self, *keys):
		# Returns a VGroup of the glyphs at the given addresses
		if MANIM_TYPE == 'GL':
			parent = self.mob
		elif MANIM_TYPE == 'CE':
			parent = self.mob[0]
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")
		
		result = VGroup()
		for key in keys:
			if isinstance(key, (int, slice)):
				result.add(*parent[key])
			elif isinstance(key, str):
				result.add(*[parent[g] for g in self.get_glyphs_at_address(key)])
			else:
				raise ValueError(f"Invalid key: {key}")
		return result


	### Addresses ###

	def get_all_addresses(self):
		# Returns the addresses of all subexpressions
		addresses = [""]
		for n in range(len(self.children)):
			for child_address in self.children[n].get_all_addresses():
				addresses.append(str(n)+child_address)
		return sorted(list(set(addresses)))
	
	def get_all_nonleaf_addresses(self):
		return sorted(list(set(a[:-1] for a in self.get_all_addresses() if a != "")))
	
	def get_all_leaf_addresses(self):
		return sorted(list(set(self.get_all_addresses()) - set(self.get_all_nonleaf_addresses())))

	def get_all_addresses_with_condition(self, condition):
		result = set()
		for address in self.get_all_addresses():
			if condition(self.get_subex(address)):
				result |= {address}
		return sorted(list(result))
	
	def get_all_addresses_of_type(self, expression_type):
		return self.get_all_addresses_with_condition(lambda subex: isinstance(subex, expression_type))

	def get_addresses_of_subex(self, target_subex):
		return self.get_all_addresses_with_condition(lambda subex: subex.is_identical_to(target_subex))


	### Subexpressions ###

	def get_subex(self, address_string):
		# Returns the Expression object corresponding to the subexpression at the given address.
		if address_string == "":
			return self
		elif int(address_string[0]) < len(self.children):
			return self.children[int(address_string[0])].get_subex(address_string[1:])
		else:
			raise IndexError(f"No subexpression of {self} at address {address_string} .")

	def get_all_subexpressions_with_condition(self, condition):
		result = set()
		for address in self.get_all_addresses():
			if condition(subex := self.get_subex(address)):
				result |= {subex}
		return result

	def get_all_subexpressions(self):
		return self.get_all_subexpressions_with_condition(lambda subex: True)

	def get_all_subexpressions_of_type(self, expression_type):
		return self.get_all_subexpressions_with_condition(lambda subex: isinstance(subex, expression_type))
	
	def get_all_variables(self):
		from .variables import Variable
		return self.get_all_subexpressions_of_type(Variable)


	### Glyphs ###

	special_character_to_glyph_method_dict = {
		# Class dictionary mapping special characters to methods
		# When a character is seen in an address, the corresponding method is called
		# Subclasses can add entries to this dictionary
		'(': 'get_left_paren_glyphs',
		')': 'get_right_paren_glyphs',
		'_': 'get_exp_glyphs_without_parentheses',
	}
	
	def number_of_glyphs(self):
		# Set this value in subclasses so as not to need to render latex
		if self._number_of_glyphs is None:
			self.init_number_of_glyphs_from_mob()
		return self._number_of_glyphs
	
	def init_number_of_glyphs_from_mob(self):	
		if MANIM_TYPE == 'GL':
			self._number_of_glyphs = len(self.mob)
		elif MANIM_TYPE == 'CE':
			self._number_of_glyphs = len(self.mob[0])
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")

	def get_glyphs_at_addigit(self, addigit:int):
		raise NotImplementedError #Implement in subclasses

	def get_glyphs_at_address(self, address):
		# Returns the list of glyph indices at the given address
		if len(address) == 0:
			return list(range(self.number_of_glyphs()))

		addigit = address[0]
		remainder = address[1:]
		result = []

		if addigit in self.special_character_to_glyph_method_dict:
			glyph_method = getattr(self, self.special_character_to_glyph_method_dict[addigit])
			result += glyph_method()
			if remainder:
				result += self.get_glyphs_at_address(remainder)
			return list(set(result))

		else:
			try:
				digit = int(addigit)
				child_glyphs = self.get_glyphs_at_addigit(digit)
				child = self.children[digit]
				glyphs_within_child = child.get_glyphs_at_address(remainder)
				shift_value = child_glyphs[0]
				result = [glyph + shift_value for glyph in glyphs_within_child]
				return list(set(result))
			except:
				raise ValueError(f"Invalid address: {address}")

	def get_glyphs_at_addresses(self, *addresses):
		result = []
		for address in addresses:
			result += self.get_glyphs_at_address(address)
		return list(set(result))

	def get_left_paren_glyphs(self):
		if not self.parentheses:
			return []
		start = 0
		end = start + self.paren_length()
		return list(range(start, end))

	def get_right_paren_glyphs(self):
		if not self.parentheses:
			return []
		end = self.number_of_glyphs()
		start = end - self.paren_length()
		return list(range(start, end))
	
	def get_exp_glyphs_without_parentheses(self):
		start = 0
		end = self.number_of_glyphs()
		if self.parentheses:
			start += self.paren_length()
			end -= self.paren_length()
		return list(range(start, end))

	def __len__(self):
		return self.number_of_glyphs()


	### Operations ###

	def __neg__(self):
		from .operations import Negative
		return Negative(self)

	def __add__(self, other):
		from .operations import Add
		return Add(self, other)

	def __radd__(self, other):
		from .operations import Add
		return Add(other, self)

	def __sub__(self, other):
		from .operations import Sub
		return Sub(self, other)

	def __rsub__(self, other):
		from .operations import Sub
		return Sub(other, self)

	def __mul__(self, other):
		from .operations import Mul
		return Mul(self, other)

	def __rmul__(self, other):
		from .operations import Mul
		return Mul(other, self)

	def __truediv__(self, other):
		from .operations import Div
		return Div(self, other)

	def __rtruediv__(self, other):
		from .operations import Div
		return Div(other, self)

	def __pow__(self, other):
		from .operations import Pow
		return Pow(self, other)

	def __rpow__(self, other):
		from .operations import Pow
		return Pow(other, self)

	def __and__(self, other):
		from .relations import Equation
		return Equation(self, other)
	
	def __rand__(self, other):
		from .relations import Equation
		return Equation(other, self)

	def __or__(self, other):
		from .relations import Equation
		return Equation(self, other)
	
	def __ror__(self, other):
		from .relations import Equation
		return Equation(other, self)

	def __rshift__(self, other):
		other = Smarten(other)
		from ..actions.action_core import Action
		from ..timelines.timeline_core import Timeline
		if isinstance(other, Expression):
			timeline = Timeline()
			timeline.add_expression_to_end(self).add_expression_to_end(other)
			return timeline
		elif isinstance(other, Action):
			timeline = Timeline()
			timeline.add_expression_to_end(self).add_action_to_end(other)
			return timeline
		else:
			return NotImplemented

	def __rrshift__(self, other):
		return Smarten(other).__rshift__(self)


	### Parentheses ###

	def give_parentheses(self, parentheses=True):
		change = parentheses - self.parentheses
		if change:
			self._mob = None # Don't init mob just yet, just mark it as needing to be reinitialized
			if self._number_of_glyphs is not None: # Adjust cached number of glyphs according to change
				self._number_of_glyphs += 2 * change * self.paren_length()
			self.parentheses = parentheses
		return self

	def clear_all_parentheses(self):
		for c in self.children:
			c.clear_all_parentheses()
		self.give_parentheses(False)
		return self

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()
		return self
	
	def reset_parentheses(self):
		self.clear_all_parentheses()
		self.auto_parentheses()
		return self

	def paren_length(self):
		# Returns the number of glyphs taken up by the expression's potential parentheses.
		# Usually 1 but can be larger for larger parentheses.
		if algebra_config['fast_paren_length'] == True:
			return 1
		yes_paren = self.copy().give_parentheses(True)
		no_paren = self.copy().give_parentheses(False)
		num_paren_glyphs = len(yes_paren) - len(no_paren)
		assert num_paren_glyphs > 0 and num_paren_glyphs % 2 == 0
		return num_paren_glyphs // 2
	
	@staticmethod
	def parenthesize(str_func):
		# To decorate most subclasses' __str__ methods
		def wrapper(expr, *args, **kwargs):
			pretex = str_func(expr, *args, **kwargs)
			if expr.parentheses:
				pretex = "\\left(" + pretex + "\\right)"
			return pretex
		return wrapper


	### Substitution ###

	def substitute_at_address(self, subex, address):
		subex = Smarten(subex).copy() #?
		if len(address) == 0:
			return subex
		index = int(address[0])
		result = self.copy()
		new_child = result.children[index].substitute_at_address(subex, address[1:])
		result.children[index] = new_child
		return result

	def substitute_at_addresses(self, subex, addresses):
		result = self.copy()
		for address in addresses:
			result = result.substitute_at_address(subex, address)
		return result

	def substitute(self, expression_dict):
		result = self.copy()
		dict_with_numbers = list(enumerate(expression_dict.items()))
		from .variables import Variable
		for i, (from_subex, to_subex) in dict_with_numbers:
			result = result.substitute_at_addresses(Variable(f"T_{i}"), result.get_addresses_of_subex(from_subex))
		for i, (from_subex, to_subex) in dict_with_numbers:
			result = result.substitute_at_addresses(to_subex, result.get_addresses_of_subex(Variable(f"T_{i}")))
		return result

	def __matmul__(self, expression_dict):
		return self.substitute(expression_dict)


	### Nesting ###
	# These do not work yet, regrettably
	def nest(self, direction="right", recurse=True):
		if len(self.children) <= 2:
			return self
		else:
			if direction == "right":
				return type(self)(self.children[0], type(self)(*self.children[1:]).nest(direction, recurse))
			elif direction == "left":
				return type(self)(type(self)(*self.children[:-1]).nest(direction, recurse), self.children[-1])
			else:
				raise ValueError(f"Invalid direction: {direction}. Must be right or left.")

	def denest(self, denest_all = False, match_type = None):
		if len(self.children) <= 1:
			return self
		if match_type is None:
			match_type = type(self)
		new_children = []
		for child in self.children:
			if type(child) == match_type:
				for grandchild in child.children:
					new_children.append(grandchild.denest(denest_all, match_type))
			elif denest_all:
				new_children.append(child.denest(True, match_type))
			else:
				new_children.append(child)
		return type(self)(*new_children)


	### Coloring ###

	def set_color_by_subex(self, subex_color_dict):
		for subex, color in subex_color_dict.items():
			for ad in self.get_addresses_of_subex(subex):
				self.get_subex(ad).color = color
				if self.get_subex(ad).parentheses and not subex.parentheses:
					ad += '_'
				self[ad].set_color(color)
		return self

	def get_color_of_subex(self, subex): # This is awful lol
		for ad in self.get_addresses_of_subex(subex):
			subex = self.get_subex(ad)
			if hasattr(subex, 'color'):
				return subex.color		



	### Utilities ###
	
	def copy(self):
		return deepcopy(self)

	def __repr__(self):
		return type(self).__name__ + "(" + str(self) + ")"

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		return type(self) == type(other) and len(self.children) == len(other.children) \
			and all(self.children[i].is_identical_to(other.children[i]) for i in range(len(self.children)))

	def evaluate(self):
		return Smarten(self.compute())




class Combiner(Expression):
	def __init__(self, symbol, symbol_glyph_length, children, **kwargs):
		super().__init__(children=children, **kwargs)
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		self.left_spacing = ""
		self.right_spacing = ""
		self._number_of_glyphs = sum([
			sum(child.number_of_glyphs() for child in self.children),
			self.symbol_glyph_length * (len(self.children) - 1),
			self.parentheses * self.paren_length() * 2
		])

	@Expression.parenthesize
	def __str__(self, *args, **kwargs):
		joiner = self.left_spacing + self.symbol + self.right_spacing
		return joiner.join(["{" + str(child) + "}" for child in self.children])

	def set_spacing(self, left_spacing, right_spacing):
		self.left_spacing = left_spacing
		self.right_spacing = right_spacing

	special_character_to_glyph_method_dict = {
		**Expression.special_character_to_glyph_method_dict,
		'+': 'get_op_glyphs',
		'-': 'get_op_glyphs',
		'*': 'get_op_glyphs',
		'/': 'get_op_glyphs',
		'^': 'get_op_glyphs',
		'=': 'get_op_glyphs',
		'<': 'get_op_glyphs',
		'>': 'get_op_glyphs',
		',': 'get_op_glyphs',
	}

	def get_glyphs_at_addigit(self, addigit:int):
		start = 0
		start += self.parentheses * self.paren_length()
		for sibling in self.children[:addigit]:
			start += sibling.number_of_glyphs()
			start += self.symbol_glyph_length
		child = self.children[addigit]
		end = start + child.number_of_glyphs()
		return list(range(start, end))

	def get_op_glyphs(self):
		results = []
		turtle = self.parentheses * self.paren_length()
		for child in self.children[:-1]:
			turtle += child.number_of_glyphs()
			results += list(range(turtle, turtle + self.symbol_glyph_length))
			turtle += self.symbol_glyph_length
		return results





class Address(str):
	pass
