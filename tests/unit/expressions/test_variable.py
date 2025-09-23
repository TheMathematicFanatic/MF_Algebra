from conftest import *


x = Variable('x')
y = Variable('y')
theta = Variable('\\theta')
a12 = Subscript(Variable('a'), 12)


@MFparam('var, num', [
	('x', x, 1),
	('y', y, 1),
	('greek', theta, 1),
	('subscript', a12, 3),
	('given', Variable('yourmom', symbol_glyph_length=581), 581)
])
def test_glyph_count(var, num):
	assert var.glyph_count == num

