from .algebra_core import AlgebraicAction
from ...expressions.variables import a
from MF_Tools.dual_compatibility import FadeIn, FadeOut, Write


class SimplificationRule(AlgebraicAction):
	pass



class add_zero_R(SimplificationRule):
	template1 = a + 0
	template2 = a
	addressmap = [['+1', FadeOut]]

class add_zero_L(SimplificationRule):
	template1 = 0 + a
	template2 = a
	addressmap = [['+0', FadeOut]]

class sub_zero_R(SimplificationRule):
	template1 = a - 0
	template2 = a
	addressmap = [['-1', FadeOut]]

class sub_zero_L(SimplificationRule):
	template1 = 0 - a
	template2 = -a
	addressmap = [['0', FadeOut], ['-', '-']]

class mul_zero_R(SimplificationRule):
	template1 = a * 0
	template2 = 0
	addressmap = [['*0', FadeOut]]

class mul_zero_L(SimplificationRule):
	template1 = 0 * a
	template2 = 0
	addressmap = [['*1', FadeOut]]

class mul_one_L(SimplificationRule):
	template1 = 1 * a
	template2 = a
	addressmap = [['*0', FadeOut]]

class mul_one_R(SimplificationRule):
	template1 = a * 1
	template2 = a
	addressmap = [['*1', FadeOut]]

class div_one_R(SimplificationRule):
	template1 = a / 1
	template2 = a
	addressmap = [['/1', FadeOut]]

class pow_one_R(SimplificationRule):
	template1 = a ** 1
	template2 = a
	addressmap = [['^1', FadeOut]]

class pow_one_R(SimplificationRule):
	template1 = 1 ** a
	template2 = 1
	addressmap = [['^1', FadeOut]]

class pow_zero_R(SimplificationRule):
	template1 = a ** 0
	template2 = 1
	addressmap = [['', '']]
