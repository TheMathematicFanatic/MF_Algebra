from .algebra_core import AlgebraicAction
from ..expressions import a, b, n, x, y, Rad, Log


class SimplificationRule(AlgebraicAction):
	pass

	# I think this is positively brilliant
	# But it is highly regrettable that static linters do not support this
	# because they don't know that the instances have been defined...
	# Oh well, I can still use this in terminal
	# and can make new instances in py files
	def __init_subclass__(cls):
		super().__init_subclass__()
		name = cls.__name__
		if name.endswith('_'):
			globals()[name[:-1]] = cls()
		


class add_zero_R_(SimplificationRule):
	template1 = a + 0
	template2 = a
	addressmap = [['+1', []]]

class add_zero_L_(SimplificationRule):
	template1 = 0 + a
	template2 = a
	addressmap = [['+0', []]]

class sub_zero_R_(SimplificationRule):
	template1 = a - 0
	template2 = a
	addressmap = [['-1', []]]

class sub_zero_L_(SimplificationRule):
	template1 = 0 - a
	template2 = -a
	addressmap = [['0', []], ['-', '-']]

class sub_same_(SimplificationRule):
	template1 = a - a
	template2 = 0
	addressmap = [['', '']]

class mul_zero_R_(SimplificationRule):
	template1 = a * 0
	template2 = 0
	addressmap = [['*0', []]]

class mul_zero_L_(SimplificationRule):
	template1 = 0 * a
	template2 = 0
	addressmap = [['*1', []]]

class mul_one_L_(SimplificationRule):
	template1 = 1 * a
	template2 = a
	addressmap = [['*0', []]]

class mul_one_R_(SimplificationRule):
	template1 = a * 1
	template2 = a
	addressmap = [['*1', []]]

class div_one_R_(SimplificationRule):
	template1 = a / 1
	template2 = a
	addressmap = [['/1', []]]

class div_zero_L_(SimplificationRule):
	template1 = 0 / a
	template2 = 0
	addressmap = [['/1', []]]

class div_same_(SimplificationRule):
	template1 = a / a
	template2 = 1
	addressmap = [['', '']]

class pow_one_R_(SimplificationRule):
	template1 = a ** 1
	template2 = a
	addressmap = [['^1', []]]

class pow_one_L_(SimplificationRule):
	template1 = 1 ** a
	template2 = 1
	addressmap = [['^1', []]]

class pow_zero_R_(SimplificationRule):
	template1 = a ** 0
	template2 = 1
	addressmap = [['', '']]

class pow_zero_L_(SimplificationRule):
	template1 = 0 ** a
	template2 = 0
	addressmap = [['^1', []]]



# Inverses

class add_sub_(SimplificationRule):
	template1 = a + b - b
	template2 = a
	addressmap = [['-0+', []]]

class sub_add_(SimplificationRule):
	template1 = a - b + b
	template2 = a
	addressmap = [['+0-', []]]

class mul_div_(SimplificationRule):
	template1 = a * b / b
	template2 = a
	addressmap = [['/0*', []]]

class div_mul_(SimplificationRule):
	template1 = a / b * b
	template2 = a
	addressmap = [['*0/', []]]

class pow_root_(SimplificationRule):
	template1 = Rad(b)(a**b)
	template2 = a
	addressmap = [['0f', []]]

class root_pow_(SimplificationRule):
	template1 = Rad(b)(a) ** b
	template2 = a
	addressmap = [['00f', []]]

class exp_log_(SimplificationRule):
	template1 = Log(b)(b**a)
	template2 = a
	addressmap = [['0f', []]]

class log_exp_(SimplificationRule):
	template1 = b ** Log(b)(a)
	template2 = a
	addressmap = [['10f', []]]



# Exponent Properties

class pow_mul_(SimplificationRule):
	template1 = x**a * x**b
	template2 = x**(a+b)
	addressmap = [['*', '1+']]
	var_kwarg_dict = {x:{'path_arc':-2}}

class pow_div_(SimplificationRule):
	template1 = x**a / x**b
	template2 = x**(a-b)
	addressmap = [['/', '1-']]
	var_kwarg_dict = {x:{'path_arc':-2}}

class mul_pow_(SimplificationRule):
	template1 = (a*b)**n
	template2 = a**n * b**n
	addressmap = [['0*', '*']]

class div_pow_(SimplificationRule):
	template1 = (a/b)**n
	template2 = a**n / b**n
	addressmap = [['0/', '/']]

class pow_pow_(SimplificationRule):
	template1 = (x**a)**b
	template2 = x**(a*b)
	addressmap = []

class neg_neg_(SimplificationRule):
	template1 = -(-a)
	template2 = a
	addressmap = [['-0-', []]]

class neg_pow_A_(SimplificationRule):
	template1 = x**-n
	template2 = 1/x**n
	addressmap = [['1-', '/'], [[], '0']] # Stylish!

class neg_pow_B_(SimplificationRule):
	template1 = (a/b)**-n
	template2 = (b/a)**n
	addressmap = [['1-', []]]



# Radical Properties

class root_to_power_A_(SimplificationRule):
	template1 = Rad(n)(x)
	template2 = x**(1/n)
	addressmap = [['0f','1/'], [[], '10', {'delay':0.5}]]

class root_to_power_B_(SimplificationRule):
	template1 = Rad(b)(x**a)
	template2 = x**(a/b)
	addressmap = [['0f', '1/']]

class root_mul_(SimplificationRule):
	template1 = Rad(n)(a*b)
	template2 = Rad(n)(a) * Rad(n)(b)
	addressmap = [['1*','*'], ['0f','00f'], ['0f','10f']]

class root_div_(SimplificationRule):
	template1 = Rad(n)(a/b)
	template2 = Rad(n)(a) / Rad(n)(b)
	addressmap = [['1/','/'], ['0f','00f'], ['0f','10f']]



# Log Properties

class log_mul_(SimplificationRule):
	template1 = Log(b)(x*y)
	template2 = Log(b)(x) + Log(b)(y)
	addressmap = [['1*','+'], ['0f','00f'], ['0f','10f']]

class log_div_(SimplificationRule):
	template1 = Log(b)(x/y)
	template2 = Log(b)(x) - Log(b)(y)
	addressmap = [['1*','+'], ['0f','00f'], ['0f','10f']]

class log_pow_(SimplificationRule):
	template1 = Log(b)(x**a)
	template2 = a*Log(b)(x)
	addressmap = [['1^','*'], ['0f','10f']]
	var_kwarg_dict = {a:{'path_arc':3}}

class log_change_base_(SimplificationRule):
	template1 = Log(a)(x)
	template2 = Log(b)(x) / Log(b)(a)
	addressmap = [['0f','00f'], ['0f','10f'], [[],'/']]






