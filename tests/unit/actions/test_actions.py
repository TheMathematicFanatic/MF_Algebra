from conftest import *

x
A = x**2 + y**2
B = 10 - A
C = (3+x)*B
D = A/B
E = A**(3-x)
func = f(x,y,z)
fg = f@g
a12 = Subscript(a, 12)

swap = swap_children_()
add = add_(5)
sub = sub_(9)
mul = mul_(18+x)
div = div_(z+y**3)
pow = pow_(-3)
subs = substitute_({x:1, y:2, z:3})
ev = evaluate_()


# def strip_addressmap(addressmap):
#     return ([entry[0], entry[1]] for entry in addressmap)
# def equal_addressmap(addressmap1, addressmap2):
#     return set(strip_addressmap(addressmap1)) == set(strip_addressmap(addressmap2))


@MFparam('in_exp, act, expected', [

    ('swap_add', A, swap, y**2 + x**2),

    ('swap_sub', B, swap, A - 10),

    ('swap_mul', C, swap, B*(3+x)),

    ('swap_div', D, swap, B/A),

    ('swap_pow', E, swap, (3-x)**A),

    ('swap_comp', f@g, swap, g@f),

    ('swap_subscript', a12, swap, Subscript(12,a)),

    ('add', A, add, A + 5),

    ('sub', A, sub, A - 9),

    ('mul', A, mul, A * (18+x)),

    ('div', A, div, A / (z+y**3)),

    ('pow', A, pow, A ** -3),

    ('substitute', A, subs, one**2 + two**2),

])
def test_get_output_expression(in_exp, act, out_exp):
    assert (in_exp >= act) == act.get_output_expression(in_exp) == out_exp


# @MFparam('in_exp, act, addressmap', [
#     ('swap_add', A, swap, (['0', '1'], ['1', '0'])),
# ])
# def test_get_addressmap(in_exp, act, addressmap):
#     admap = act.get_addressmap(in_exp)
#     assert admap == act.get_addressmap(act <= in_exp)
#     assert equal_addressmap(admap, addressmap)