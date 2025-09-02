# expressions.py
from MF_Tools.dual_compatibility import dc_Tex as Tex, MANIM_TYPE, VGroup
from ..utils import Smarten, add_spaces_around_brackets, parenthesize
from copy import deepcopy


algebra_config = {
		"auto_parentheses": True,
		"multiplication_mode": "auto",
		"division_mode": "fraction",
		"decimal_precision": 4,
		"always_color": {},
		"fast_paren_length": False
	}

class Expression:
	def __init__(self, parentheses=False, **kwargs):
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		self._mob = None

	@property
	def mob(self):
		if self._mob is None:
			self.init_mob()
		return self._mob

	def init_mob(self, **kwargs):
		string = add_spaces_around_brackets(str(self))
		self._mob = Tex(string, **kwargs)
		self.set_color_by_subex(algebra_config["always_color"])
	
	def copy(self):
		return deepcopy(self)

	def __getitem__(self, *key):
		if isinstance(key, str): # address of subexpressions, should return the glyphs corresponding to that subexpression
			if MANIM_TYPE == 'GL':
				return VGroup(*[self.mob[g] for g in self.get_glyphs(key)])
			elif MANIM_TYPE == 'CE':
				return VGroup(*[self.mob[0][g] for g in self.get_glyphs(key)])
			else:
				raise Exception(f"Unknown manim type: {MANIM_TYPE}")
		else: # preserve behavior of Tex indexing
			return self.mob.__getitem__(key)

	def get_all_addresses(self):
		# Returns the addresses of all subexpressions
		addresses = [""]
		for n in range(len(self.children)):
			for child_address in self.children[n].get_all_addresses():
				addresses.append(str(n)+child_address)
		return addresses
	
	def get_all_nonleaf_addresses(self):
		return sorted(list({a[:-1] for a in self.get_all_addresses() if a != ""}))
	
	def get_all_leaf_addresses(self):
		return sorted(list(set(self.get_all_addresses()) - set(self.get_all_nonleaf_addresses())))

	def get_subex(self, address_string):
		# Returns the Expression object corresponding to the subexpression at the given address.
		# Note that this is not a submobject of self! It is a different mobject probably not on screen,
		# it was just created to help create self.
		if address_string == "":
			return self
		elif int(address_string[0]) < len(self.children):
			return self.children[int(address_string[0])].get_subex(address_string[1:])
		else:
			raise IndexError(f"No subexpression of {self} at address {address_string} .")

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		return type(self) == type(other) and len(self.children) == len(other.children) \
			and all(self.children[i].is_identical_to(other.children[i]) for i in range(len(self.children)))

	def get_addresses_of_subex(self, subex):
		subex = Smarten(subex)
		addresses = []
		for ad in self.get_all_addresses():
			if self.get_subex(ad).is_identical_to(subex):
				addresses.append(ad)
		return addresses


	'''
	Glyph Related Matters
	'''

	special_character_to_glyph_method_dict = {
		'(': 'get_left_paren_glyphs',
		')': 'get_right_paren_glyphs',
		'_': 'get_exp_glyphs_without_parentheses',
	}

	def number_of_glyphs(self):
		# Optimize in subclasses so as not to need to render latex
		if MANIM_TYPE == 'GL':
			return len(self.mob)
		elif MANIM_TYPE == 'CE':
			return len(self.mob[0])
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")

	def get_glyphs_at_address(self, address):
		if address == "":
			return list(range(self.number_of_glyphs()))
		first_character = address[0]
		remainder = address[1:]
		result = []
		if first_character in self.special_character_to_glyph_method_dict:
			glyph_method = getattr(self, self.special_character_to_glyph_method_dict[first_character])
			result += glyph_method()
			if remainder:
				result += self.get_glyphs_at_address(remainder)
			return list(set(result))
		elif first_character in '0123456789':
			digit = int(first_character)
			child_glyphs = self.get_glyphs_at_addigit(digit)
			child = self.children[digit]
			glyphs_within_child = child.get_glyphs_at_address(remainder)
			shift_value = child_glyphs[0] - (self.paren_length() if self.parentheses else 0)
			result = [glyph + shift_value for glyph in glyphs_within_child]
			return list(set(result))
		else:
			raise ValueError(f"Invalid address: {address}")

	def get_glyphs(self, *addresses):
		result = []
		for address in addresses:
			result += self.get_glyphs_at_address(address)
		return list(set(result))

	def get_left_paren_glyphs(self):
		if not self.parentheses:
			return []
		start = 0
		end = self.paren_length()
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

	def __neg__(self):
		from .operations import Negative
		return Negative(self)

	def __add__(self, other):
		from .operations import Add
		return Add(self, other)

	def __sub__(self, other):
		from .operations import Sub
		return Sub(self, other)

	def __mul__(self, other):
		from .operations import Mul
		return Mul(self, other)

	def __truediv__(self, other):
		from .operations import Div
		return Div(self, other)

	def __pow__(self, other):
		from .operations import Pow
		return Pow(self, other)

	def __radd__(self, other):
		from .operations import Add
		return Add(other, self)

	def __rsub__(self, other):
		from .operations import Sub
		return Sub(other, self)

	def __rmul__(self, other):
		from .operations import Mul
		return Mul(other, self)

	def __rtruediv__(self, other):
		from .operations import Div
		return Div(other, self)

	def __rpow__(self, other):
		from .operations import Pow
		return Pow(other, self)

	def __matmul__(self, expression_dict):
		return self.substitute(expression_dict)

	def __and__(self, other):
		from .relations import Equation
		return Equation(self, other)
	
	def __rand__(self, other):
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

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def give_parentheses(self, parentheses=True):
		self.parentheses = parentheses
		self._mob = None # Don't init mob just yet, just mark it as needing to be reinitialized
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

	#Man these guys do not work correctly yet
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

	def set_color_by_subex(self, subex_color_dict):
		for subex, color in subex_color_dict.items():
			for ad in self.get_addresses_of_subex(subex):
				self.get_subex(ad).color = color
				self[ad].set_color(color)
				if self.get_subex(ad).parentheses and not subex.parentheses:
					self[ad+"()"].set_color(self.color)
		return self

	def get_color_of_subex(self, subex): # This is awful lol
		for ad in self.get_addresses_of_subex(subex):
			subex = self.get_subex(ad)
			if hasattr(subex, 'color'):
				return subex.color		

	def evaluate(self):
		return Smarten(self.compute())

	def __repr__(self):
		return type(self).__name__ + "(" + str(self) + ")"

	def get_all_subexpressions_of_type(self, expression_type):
		result = set()
		for child in self.children:
			if isinstance(child, expression_type):
				result |= {child}
			else:
				result |= child.get_all_subexpressions_of_type(expression_type)
		return result
	
	def get_all_variables(self):
		from .variables import Variable
		return self.get_all_subexpressions_of_type(Variable)



class Combiner(Expression):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		self.children = list(map(Smarten,children))
		self.left_spacing = ""
		self.right_spacing = ""
		super().__init__(**kwargs)

	@parenthesize
	def __str__(self, *args, **kwargs):
		joiner = self.left_spacing + self.symbol + self.right_spacing
		result = joiner.join(["{" + str(child) + "}" for child in self.children])
		return result

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

	def get_glyphs_at_addigit(self, addigit):
		child_index = int(addigit)
		start = 0
		if self.parentheses:
			start += self.paren_length()
		for sibling in self.children[:child_index]:
			start += sibling.number_of_glyphs()
			start += self.symbol_glyph_length
		child = self.children[child_index]
		end = start + child.number_of_glyphs()
		return list(range(start, end))

	def get_op_glyphs(self):
		results = []
		turtle = 0
		for child in self.children[:-1]:
			turtle += child.number_of_glyphs()
			results += list(range(turtle, turtle + self.symbol_glyph_length))
			turtle += self.symbol_glyph_length
		return results
