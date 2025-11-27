from conftest import *


def test_function_children():
	S = Sum(n,0,108)
	a = x**n / fact(n)
	Sa = S(a)
	assert Sa.children[0] == S
	assert Sa.children[1] == a
	assert S.get_glyphs_at_addigit(1) == [0,1,2]
	assert S.get_glyphs_at_addigit(0) == [4,5,6]