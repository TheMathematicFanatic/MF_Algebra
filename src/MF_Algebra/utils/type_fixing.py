import numpy as np
from .config import algebra_config


def Smarten(input):
	if input is None:
		return None

	from .base_class import MF_Base
	if isinstance(input, MF_Base):
		return input.copy()

	if isinstance(input, int):
		from ..expressions.numbers.integer import Integer
		return Integer(input)

	if isinstance(input, float):
		if input == np.inf:
			from ..calculus.limits import inf
			return inf
		if input == np.nan:
			return None
		from math import isclose
		if isclose(input, round(input), rel_tol=0, abs_tol=algebra_config['integer_tolerance']):
			from ..expressions.numbers.integer import Integer
			return Integer(round(input))
		from ..expressions.numbers.real import Real
		return Real(input)

	if isinstance(input, complex):
		from ..expressions.numbers.complex import Complex
		return Complex(input)

	if isinstance(input, tuple):
		from ..expressions.combiners.sequences import Coordinate
		return Coordinate(*input)

	if input is ...:
		from ..expressions.variables import dots
		return dots

	from decimal import Decimal
	if isinstance(input, Decimal):
		return Smarten(float(input))

	from fractions import Fraction
	if isinstance(input, Fraction):
		from ..expressions.numbers.rational import Rational
		return Rational(input.numerator, input.denominator)

	raise NotImplementedError(f"Unsupported type {type(input)}")


