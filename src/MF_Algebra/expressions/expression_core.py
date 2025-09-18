# expressions.py
from MF_Tools.dual_compatibility import dc_Tex as Tex, MANIM_TYPE, VGroup
from ..utils import Smarten, add_spaces_around_brackets
from copy import deepcopy
from functools import wraps


algebra_config = {
	'auto_parentheses': True,
	'multiplication_mode': 'auto',
	'division_mode': 'fraction',
	'decimal_precision': 4,
	'always_color': {},
	'fast_paren_length': True,
	'fast_glyph_count': True,
	'fast_root_length': True,
}


class Expression:
	def __init__(self, children=[], parentheses=False, **kwargs):
		self.children = list(map(Smarten,children))
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		self._mob = None
		self._glyph_count = None


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

	def __getitem__(self, key):
		# Returns a VGroup of the glyphs at the given addresses
		if MANIM_TYPE == 'GL':
			parent = self.mob
		elif MANIM_TYPE == 'CE':
			parent = self.mob[0]
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")
		
		result = VGroup()
		if isinstance(key, int):
			result.add(parent[key])
		elif isinstance(key, slice):
			result.add(*parent[key])
		elif isinstance(key, str):
			result.add(*[parent[g] for g in self.get_glyphs_at_address(key)])
		elif isinstance(key, (list, tuple)):
			for k in key:
				result.add(*self[k])
		else:
			raise ValueError(f"Invalid key: {key}")
		return result


	### Glyphs ###
	@property
	def glyph_count(self):
		# Set this value in subclasses so as not to need to render latex
		if self._glyph_count is None:
			self.init_glyph_count()
		return self._glyph_count
	
	def init_glyph_count(self):
		if algebra_config['fast_glyph_count']:
			try:
				gc = self.get_glyph_count()
				assert isinstance(gc, int)
				self._glyph_count = gc
				return
			except (NotImplementedError, AssertionError, AttributeError):
				pass
		gc = self.get_glyph_count_from_mob()
		self._glyph_count = gc
	
	def get_glyph_count(self):
		# Guesses the number of glyphs in the expression, from a formula for the subclass.
		# Override in subclasses
		raise NotImplementedError
	
	def get_glyph_count_from_mob(self):	
		if MANIM_TYPE == 'GL':
			parent = self.mob
		elif MANIM_TYPE == 'CE':
			parent = self.mob[0]
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")
		return len(parent)

	special_character_to_glyph_method_dict = {
		# Class dictionary mapping special characters to methods
		# When a character is seen in an address, the corresponding method is called
		# Subclasses can add entries to this dictionary
		'(': 'get_left_paren_glyphs',
		')': 'get_right_paren_glyphs',
		'_': 'get_exp_glyphs_without_parentheses',
		'#': 'get_glyphs_at_all_children', # This would be a cool idea, so 10#1 is equivalent to 1001,1011,1021 or whatever
	}

	def get_glyphs_at_address(self, address):
		# Returns the list of glyph indices at the given address
		if len(address) == 0:
			return list(range(self.glyph_count))

		addigit = address[0]
		remainder = address[1:]
		result = []

		if addigit in self.special_character_to_glyph_method_dict:
			glyph_method = getattr(self, self.special_character_to_glyph_method_dict[addigit])
			result += glyph_method()
			if remainder:
				result += self.get_glyphs_at_address(remainder)
			return sorted(list(set(result)))

		else:
			try:
				digit = int(addigit)
				child_glyphs = self.get_glyphs_at_addigit(digit)
				if len(child_glyphs) == 0:
					return []
				child = self.children[digit]
				glyphs_within_child = child.get_glyphs_at_address(remainder)
				shift_value = child_glyphs[0]
				result = [glyph + shift_value for glyph in glyphs_within_child]
				return sorted(list(set(result)))
			except:
				raise ValueError(f"Invalid address: {address}")

	def get_glyphs_at_addresses(self, *addresses):
		result = []
		for address in addresses:
			result += self.get_glyphs_at_address(address)
		return sorted(list(set(result)))

	def get_left_paren_glyphs(self):
		if not self.parentheses:
			return []
		start = 0
		end = start + self.paren_length()
		return list(range(start, end))

	def get_right_paren_glyphs(self):
		if not self.parentheses:
			return []
		end = self.glyph_count
		start = end - self.paren_length()
		return list(range(start, end))
	
	def get_exp_glyphs_without_parentheses(self):
		start = 0
		end = self.glyph_count
		if self.parentheses:
			start += self.paren_length()
			end -= self.paren_length()
		return list(range(start, end))

	def __len__(self):
		return self.glyph_count

	def get_glyphs_at_addigit(self, addigit:int):
		raise NotImplementedError #Implement in subclasses


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
	
	def get_all_twig_addresses(self):
		return sorted(list(set(a[:-1] for a in self.get_all_leaf_addresses() if a != "")))

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

	def get_all_numbers(self):
		from .numbers.number import Number
		return self.get_all_subexpressions_of_type(Number)


	### Operations ###

	def __neg__(self):
		from .combiners.operations import Negative
		return Negative(self)

	def __add__(self, other):
		from .combiners.operations import Add
		return Add(self, other)

	def __radd__(self, other):
		from .combiners.operations import Add
		return Add(other, self)

	def __sub__(self, other):
		from .combiners.operations import Sub
		return Sub(self, other)

	def __rsub__(self, other):
		from .combiners.operations import Sub
		return Sub(other, self)

	def __mul__(self, other):
		from .combiners.operations import Mul
		return Mul(self, other)

	def __rmul__(self, other):
		from .combiners.operations import Mul
		return Mul(other, self)

	def __truediv__(self, other):
		from .combiners.operations import Div
		return Div(self, other)

	def __rtruediv__(self, other):
		from .combiners.operations import Div
		return Div(other, self)

	def __pow__(self, other):
		from .combiners.operations import Pow
		return Pow(self, other)

	def __rpow__(self, other):
		from .combiners.operations import Pow
		return Pow(other, self)

	def __and__(self, other):
		from .combiners.relations import Equation
		return Equation(self, other)
	
	def __rand__(self, other):
		from .combiners.relations import Equation
		return Equation(other, self)

	def __or__(self, other):
		from .combiners.relations import Equation
		return Equation(self, other)
	
	def __ror__(self, other):
		from .combiners.relations import Equation
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

	def subscript(self, subscript):
		from .combiners.subscripts import Subscript
		return Subscript(self, subscript)


	### Parentheses ###

	def give_parentheses(self, parentheses=True):
		change = parentheses - self.parentheses
		if change:
			self._mob = None # Don't init mob just yet, just clear the cached mob
			if algebra_config['fast_glyph_count'] and self._glyph_count is not None:
				# Adjust cached number of glyphs according to change
				self._glyph_count += 2 * change * self.paren_length()
			else:
				# Otherwise just clear the cache
				self._glyph_count = None
			self.parentheses = parentheses
		return self

	def clear_all_parentheses(self):
		for child in self.children:
			child.clear_all_parentheses()
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
		num_paren_glyphs = yes_paren.glyph_count - no_paren.glyph_count
		assert num_paren_glyphs > 0 and num_paren_glyphs % 2 == 0
		return num_paren_glyphs // 2
	
	@staticmethod
	def parenthesize_latex(str_func):
		# To decorate most subclasses' __str__ methods
		@wraps(str_func)
		def wrapper(expr, *args, **kwargs):
			pretex = str_func(expr, *args, **kwargs)
			if expr.parentheses:
				pretex = "\\left(" + pretex + "\\right)"
			return pretex
		return wrapper

	@staticmethod
	def parenthesize_glyph_count(gc_func):
		# To decorate most subclasses' get_glyph_count methods
		@wraps(gc_func)
		def wrapper(expr, *args, **kwargs):
			gc = gc_func(expr, *args, **kwargs)
			if isinstance(gc, int) and expr.parentheses:
				gc += 2 * expr.paren_length()
			return gc
		return wrapper


	### Substitution ###

	def substitute_at_address(self, subex, address):
		subex = Smarten(subex)
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
		return type(self).__name__ + "(" + self.repr_string() + ")"
	
	def repr_string(self):
		return self.__class__.__str__.__wrapped__(self) # Can be overriden in subclasses with an annoying latex string

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		other = Smarten(other)
		return all([
			type(self) == type(other),
			len(self.children) == len(other.children),
			*[
				self.children[i].is_identical_to(other.children[i])
				for i in range(len(self.children))
			]
		])

	def compute(self):
		# Define for operations, functions, etc
		raise NotImplementedError

	def evaluate(self):
		return Smarten(self.compute())

	@property
	def sympy(self):
		from sympy.parsing.latex import parse_latex
		return parse_latex(str(self))



class Address(str):
	pass
