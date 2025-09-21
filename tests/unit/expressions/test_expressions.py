from conftest import *


x
add = a+5
sub = y-9
mul = 9*z
div = n/12
pow = b**-3
A = x**2 + y**2
B = 10 - A
func = f(x,y,z)
a12 = a.subscript(12)


@MFparam('exp, count', [

	('var', x, 1),

	('var_subscript', a12, 3),

	('var_given', Variable('\\gamma', symbol_glyph_length=581), 581),

	('integer', Integer(-120), 4),

	('add', add, 3),

	('sub', sub, 3),

	('mul', mul, 2),

	('div', div, 4),

	('pow', pow, 3),

	('compound1', A, 5),

	('compound2', B, 10),

	('function', func, 8),

])
def test_get_glyph_count_from_shortcut(exp, count):
	exp.init_number_of_glyphs_from_mob = None
	assert exp.glyph_count == count



@MFparam('exp, count', [

	('var', x, 1),

	('var_subscript', a12, 3),

	('var_given', Variable('\\gamma', symbol_glyph_length=581), 1),

	('integer', Integer(-120), 4),

	('add', add, 3),

	('sub', sub, 3),

	('mul', mul, 2),

	('div', div, 4),

	('pow', pow, 3),

	('compound1', A, 5),

	('compound2', B, 10),

	('function', func, 8),

])
def test_get_glyph_count_from_mob(exp, count):
	exp.get_glyph_count = lambda *args, **kwargs: None
	assert exp.glyph_count == count



@MFparam('exp, addigit, glyphs', [

	('add', add, 0, [0]),

	('sub', sub, 1, [2]),

	('mul', mul, 0, [0]),

	('div', div, 1, [2,3]),

	('pow', pow, 1, [1,2]),

	('compound1', A, 0, [0,1]),

	('compound2', B, 0, [0,1]),

	('compound3', B, 1, [3,4,5,6,7,8,9]),

	('function1', func, 0, [0]),

	('function2', func, 1, [1,2,3,4,5,6,7]),

	('subscript', a12, 0, [0]),

	('subscript', a12, 1, [1,2]),

])
def test_get_glyphs_at_addigit(exp, addigit, glyphs):
	assert exp.get_glyphs_at_addigit(addigit) == glyphs



@MFparam('exp, address, glyphs', [

	('var empty', x, '', [0]),

	('empty', A, '', [0,1,2,3,4]),

	('left', A, '0', [0,1]),

	('right', A, '1', [3,4]),

	('op', A, '+', [2]),

	('op and grandchild', A, '+11', [2,4]),

	('missing parens', A, '()', []),

	('no parens', A, '_', [0,1,2,3,4]),

	('left', B, '1', [3,4,5,6,7,8,9]),

	('left no parens', B, '1_', [4,5,6,7,8]),

	('child paren L', B, '1(', [3]),

	('child paren R', B, '1)', [9]),

	('child paren LR', B, '1()', [3,9]),

	('op', B, '-', [2]),

	('complicated pseudo', B, '-1()01', [2,3,5,9]),

	('function 1', func, '1,(2', [1,3,5,6]),

	('function 2', func, '1_)', [2,3,4,5,6,7]),

])
def test_get_glyphs_at_address(exp, address, glyphs):
	assert exp.get_glyphs_at_address(address) == glyphs



@MFparam('exp, addresses, glyphs', [

	('easy', A, ('0', '1'), [0,1,3,4]),

	('medium', B, ('0', '11', '1('), [0,1,3,7,8]),

	('hard', (a**2+b**2)/(a*b+1), ('00', '1+', '/'), [0,1,5,8])

])
def test_get_glyphs_at_addresses(exp, addresses, glyphs):
	assert exp.get_glyphs_at_addresses(*addresses) == glyphs



@MFparam('exp, addresses', [

	('var', b, ['']),

	('add', add, ['', '0', '1']),

	('compound', A, ['', '0', '00', '01', '1', '10', '11']),

	('function', func, ['', '0', '1', '10', '11', '12']),

	('subscript', a12, ['', '0', '1'])

])
def test_get_all_addresses(exp, addresses):
	assert exp.get_all_addresses() == addresses



@MFparam('exp, addresses', [

	('var', b, []),

	('add', add, ['']),

	('compound', A, ['', '0', '1']),

	('function', func, ['', '1'])

])
def test_get_all_nonleaf_addresses(exp, addresses):
	assert exp.get_all_nonleaf_addresses() == addresses



@MFparam('exp, addresses', [

	('var', b, ['']),

	('add', add, ['0', '1']),

	('compound', A, ['00', '01', '10', '11']),

	('function', func, ['0', '10', '11', '12'])

])
def test_get_all_leaf_addresses(exp, addresses):
	assert exp.get_all_leaf_addresses() == addresses



@MFparam('exp, condition, addresses', [

	('get_vars', A, lambda subex: isinstance(subex, Variable), ['00', '10']),

	('get_twos', A, lambda subex: subex.is_identical_to(2), ['01', '11']),

	('get_vars_and_twos', B, lambda subex: isinstance(subex, Variable) or subex.is_identical_to(2), ['100', '101', '110', '111']),

])
def test_get_all_addresses_with_condition(exp, condition, addresses):
	assert exp.get_all_addresses_with_condition(condition) == addresses



@MFparam('exp, type, addresses', [

	('var', theta, Variable, ['']),

	('sub', sub, Sub, ['']),

	('child_add', B, Add, ['1']),

	('child_pow', B, Pow, ['10', '11']),

	('function1', func, Function, ['0']),

	('function2', func, Sequence, ['1']),

	('function3', func, Variable, ['10', '11', '12'])

])
def test_get_all_addresses_of_type(exp, type, addresses):
	assert exp.get_all_addresses_of_type(type) == addresses



@MFparam('exp, subex, addresses', [

	('var', z, z, ['']),

	('compound1', A, A, ['']),

	('compound2', A, y**2, ['1']),

	('compound3', A, 2, ['01', '11']),

	('compound4', B, A, ['1']),

	('fail', B, z, []),

	('function', func, y, ['11'])

])
def test_get_addresses_of_subex(exp, subex, addresses):
	assert exp.get_addresses_of_subex(subex) == addresses



@MFparam('exp, address, subex', [

	('var', z, '', z),

	('add', a+9, '0', a),

	('compound1', A, '1', y**2),

	('compound2', B, '101', 2),

	('function1', func, '0', f),

	('function2', func, '1', Sequence(x,y,z)),

	('function3', func, '12', z)

])
def test_get_subex(exp, address, subex):
	assert exp.get_subex(address).is_identical_to(subex)



@MFparam('exp, condition, subexes', [

	('get_vars', A, lambda subex: isinstance(subex, Variable), {x,y}),

	('get_twos', A, lambda subex: subex.is_identical_to(2), {2}),

	('get_vars_and_twos', B, lambda subex: isinstance(subex, Variable) or subex.is_identical_to(2), {x,y,2}),

	('get_function', (3+func)**2, lambda subex: isinstance(subex, Function), {f}),

	('get_apply_function', (3+func)**2, lambda subex: isinstance(subex, ApplyFunction), {func}),

])
def test_get_all_subexpressions_with_condition(exp, condition, subexes):
	for subex1 in exp.get_all_subexpressions_with_condition(condition):
		if not any(subex1.is_identical_to(subex2) for subex2 in subexes):
			assert False



@MFparam('exp, subexes', [

	('var', b, {b}),

	('add', add, {add, a, 5}),

	('div', div, {div, n, 12}),

	('compound1', A, {A, x**2, y**2, x, y, 2}),

	('compound2', B, {B, 10, A, x**2, y**2, x, y, 2}),

	('function', func, {func, f, Sequence(x,y,z), x, y, z})

])
def test_get_all_subexpressions(exp, subexes):
	for subex1 in exp.get_all_subexpressions():
		if not any(subex1.is_identical_to(subex2) for subex2 in subexes):
			print(exp)
			print(subex1)
			print(subexes)
			assert False



@MFparam('exp, type, subexes', [

	('var', theta, Variable, {theta}),

	('sub', sub, Sub, {sub}),

	('child_add', B, Add, {A}),

	('child_pow', B, Pow, {x**2, y**2, 10}),

	('function1', func, Function, {f}),

	('function2', func, Sequence, {Sequence(x,y,z)}),

	('function3', func, Variable, {x,y,z})

])
def test_get_all_subexpressions_of_type(exp, type, subexes):
	for subex1 in exp.get_all_subexpressions_of_type(type):
		if not any(subex1.is_identical_to(subex2) for subex2 in subexes):
			assert False



@MFparam('exp, subexes', [

	('var', theta, {theta}),

	('sub', sub, {y}),

	('compound1', B, {x,y}),

	('compound2', a**b-3**c, {a,b,c}),

	('function', func, {x,y,z}),

])
def test_get_all_variables(exp, subexes):
	for subex1 in exp.get_all_variables():
		if not any(subex1.is_identical_to(subex2) for subex2 in subexes):
			assert False



@MFparam('exp, paren_length', [

	('var', Variable('x'), 1),

	('fake_given', Variable('hello', symbol_glyph_length=108), 1),

	('add', add, 1),

	('compound1', A, 1),

	('compound2', (B/B)**3, 2), # Big enough to have 2 glyphs each in mob

	('function', func, 1),

])
def test_give_parentheses_using_mob(exp, paren_length):
	exp.get_glyph_count = lambda *args, **kwargs: None
	yes_paren = exp.copy().give_parentheses(True)
	no_paren = exp.copy().give_parentheses(False)
	assert yes_paren.glyph_count - no_paren.glyph_count == 2 * paren_length
	assert str(yes_paren) == '\\left(' + str(no_paren) + '\\right)'



@MFparam('exp, paren_length', [

	('var', Variable('x', symbol_glyph_length=1), 1),

	('add', add, 1),

	('compound1', A, 1),

	('compound2', (B/B)**3, 1), # Just assumes 1 if in fast paren mode

	('function', func, 1),

])
def test_give_parentheses_without_mob(exp, paren_length):
	exp.init_number_of_glyphs_from_mob = None
	yes_paren = exp.copy().give_parentheses(True)
	no_paren = exp.copy().give_parentheses(False)
	assert yes_paren.glyph_count - no_paren.glyph_count == 2 * paren_length
	assert str(yes_paren) == '\\left(' + str(no_paren) + '\\right)'




@MFparam('exp', [

	('var', x),

	('add', add),

	('compound1', A),

	('compound2', (B/B)**3),

	('function', func)

])
def test_clear_all_parentheses(exp):
	exp.clear_all_parentheses()
	for subex in exp.get_all_subexpressions():
		assert not subex.parentheses



@MFparam('exp, child_parens', [

	('var', x, ()),

	('add1', a+5, (False, False)),

	('add2', a+-5, (False, False)), #idk

	('sub1', a-5, (False, False)),

	('sub2', 3-(a+b), (False, True)),

	('sub3', 3-(-x), (False, True)), #idk

	('mul1', a*b, (False, False)),

	('mul2', 5*(a-b), (False, True)),

	('mul3', (a+5)*(b-c), (True, True)),

	('div1', a/b, (False, False)),

	('div2', 5/(a-b), (False, False)),

	('function', func, (False, True))

])
def test_auto_parentheses(exp, child_parens):
	exp.auto_parentheses()
	assert all(exp.children[i].parentheses == child_parens[i] for i in range(len(child_parens)))



@MFparam('exp, subex, address, result', [

	('var1', x, y, '', y),

	('var2', z, A, '', A),

	('div1', n/12, 51, '1', n/51),

	('div2', n/12, 51, '0', Div(51,12)),

	('compound1', A, e**z, '1', x**2+e**z),

	('compound2', B, 3-n, '101', 10-(x**(3-n)+y**2)),

	('function1', func, 3, '1', f(3)),

	('function2', func, x*y, '12', f(x,y,x*y))

])
def test_substitute_at_address(exp, subex, address, result):
	print(result.children)
	print(exp.substitute_at_address(subex, address).children)
	assert exp.substitute_at_address(subex, address).is_identical_to(result)



@MFparam('exp, subex, addresses, result', [

	('var1', x, y, [''], y),

	('var2', z, A, [''], A),

	('div', n/12, 51, ['0', '1'], Div(51,51)),

	('compound1', A, e**z, ['00','1'], (e**z)**2+e**z),

	('compound2', B, 3-n, ['101', '110', '0'], (3-n)-(x**(3-n)+(3-n)**2)),

	('function1', func, 3, ['1'], f(3)),

	('function2', func, x**2-5, ['10', '12'], f(x**2-5,y,x**2-5))

])
def test_substitute_at_addresses(exp, subex, addresses, result):
	assert exp.substitute_at_addresses(subex, addresses).is_identical_to(result)



@MFparam('exp, substitution_dict, result', [

	('var1', x, {x: y}, y),

	('var2', x, {z: 12, x**2: 3}, x),

	('div', n/12, {n: 51}, Div(51,12)),

	('compound1', A, {x: 3, y: 4}, Integer(3)**2+Integer(4)**2),

	('compound2', B, {x**2:a, y:b}, 10-(a+b**2)),

	('compound3', B, {2:3, 3:5, x:n, z:12}, 10-(n**3+y**3)),

	('function', func, {y:y-20, z:x*y}, f(x,y-20,x*y))

])
def test_substitute(exp, substitution_dict, result):
	assert exp.substitute(substitution_dict).is_identical_to(result)
	assert (exp @ substitution_dict).is_identical_to(result)









