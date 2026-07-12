from .operations import *


class SilentAdd(BinaryOperation):
	symbol = ''
	symbol_glyph_length = 0
	eval_op = staticmethod(lambda x, y: x + y)


class SilentPositive(UnaryOperation):
	symbol = ''
	symbol_glyph_length = 0
	eval_op = staticmethod(lambda x: x)


def convert_terms_to_silent_add(nested_terms):
	def get_new_children(nested_terms):
		if not isinstance(nested_terms, (Add, Sub, PlusMinus, MinusPlus)):
			# base case
			if isinstance(nested_terms, UnaryOperation):
				return [nested_terms]
			else:
				return [SilentPositive(nested_terms)]
		else:
			left, right = nested_terms.children
			if isinstance(nested_terms, Add):
				new_child = Positive(right)
			elif isinstance(nested_terms, Sub):
				new_child = Negative(right)
			elif isinstance(nested_terms, PlusMinus):
				new_child = PositiveNegative(right)
			elif isinstance(nested_terms, MinusPlus):
				new_child = NegativePositive(right)
			else:
				raise ValueError(f'unexpected operation: {type(nested_terms)}')
			return get_new_children(left) + [new_child]
	return SilentAdd(*get_new_children(nested_terms))


def convert_silent_add_to_terms(silent_add):
	children = silent_add.children
	if isinstance(children[0], SilentPositive):
		result = children[0][0]
	else:
		result = children[0]
	for child in children[1:]:
		if isinstance(child, Positive):
			result = Add(result, child[0])
		elif isinstance(child, Negative):
			result = Sub(result, child[0])
		elif isinstance(child, PositiveNegative):
			result = PlusMinus(result, child[0])
		elif isinstance(child, NegativePositive):
			result = MinusPlus(result, child[0])
		else:
			raise ValueError(f'unexpected operation: {type(child)}')
	return result



