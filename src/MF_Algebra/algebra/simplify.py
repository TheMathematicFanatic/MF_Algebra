from .algebra_core import AlgebraicAction
from ..expressions.variables import a
from ..utils import Smarten


class SimplificationRule(AlgebraicAction):
	def __new__(cls, *args, **kwargs):
		cls.template1 = Smarten(cls.template1)
		cls.template2 = Smarten(cls.template2)
		return super().__new__(cls, *args, **kwargs)


class add_zero_R(SimplificationRule):
	template1 = a + 0
	template2 = a
	addressmap = [['+1', []]]

class add_zero_L(SimplificationRule):
	template1 = 0 + a
	template2 = a
	addressmap = [['+0', []]]

class sub_zero_R(SimplificationRule):
	template1 = a - 0
	template2 = a
	addressmap = [['-1', []]]

class sub_zero_L(SimplificationRule):
	template1 = 0 - a
	template2 = -a
	addressmap = [['0', []], ['-', '-']]

class mul_zero_R(SimplificationRule):
	template1 = a * 0
	template2 = 0
	addressmap = [['*0', []]]

class mul_zero_L(SimplificationRule):
	template1 = 0 * a
	template2 = 0
	addressmap = [['*1', []]]

class mul_one_L(SimplificationRule):
	template1 = 1 * a
	template2 = a
	addressmap = [['*0', []]]

class mul_one_R(SimplificationRule):
	template1 = a * 1
	template2 = a
	addressmap = [['*1', []]]

class div_one_R(SimplificationRule):
	template1 = a / 1
	template2 = a
	addressmap = [['/1', []]]

class div_zero_L(SimplificationRule):
	template1 = 0 / a
	template2 = 0
	addressmap = [['/1', []]]

class pow_one_R(SimplificationRule):
	template1 = a ** 1
	template2 = a
	addressmap = [['^1', []]]

class pow_one_L(SimplificationRule):
	template1 = 1 ** a
	template2 = 1
	addressmap = [['^1', []]]

class pow_zero_R(SimplificationRule):
	template1 = a ** 0
	template2 = 1
	addressmap = [['', '']]

class pow_zero_L(SimplificationRule):
	template1 = 0 ** a
	template2 = 0
	addressmap = [['^1', []]]
