from conftest import MFparam
from MF_Algebra import *


variables = [
	x := Variable('x'),
	y := Variable('y'),
	theta := Variable('\\theta'),
	a12 := Variable('a_{12}')
]

@MFparam('var, num', [
	('x', x, 1),
	('y', y, 1),
	('greek', theta, 1),
	('subscript', a12, 3),
	('given', Variable('yourmom', symbol_glyph_length=581), 581)
])
def test_number_of_glyphs(var, num):
	assert var.number_of_glyphs() == num




# @pytest.mark.parametrize('var', variables)
# def test_getitem(var):
# 	assert var[''] == var.mob




# def wrap(func):
# 	def wrapper(*args, **kwargs):
# 		print('before')
# 		out = func(*args, **kwargs)
# 		print('after')
# 		return out
# 	return wrapper

# def my_func(x):
# 	print(x, ' is good')

# my_func = wrap(my_func)

# my_func(3)