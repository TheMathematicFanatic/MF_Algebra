import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Algebra import *




A,B,C,x,y,i,n = Variables('ABCxyin')
xi = Subscript(x,i)
yi = Subscript(y,i)
S = Sum(i,0,n)
eq = S(A*(xi*yi)) | S(B*xi**2) + S(C*xi)

linear = AlgebraicAction(
    f(a*x),
    a*f(x),
    var_kwarg_dict = {a:{'path_arc':PI/2}}
)

# act = linear.both().right()
# act = linear.left() | swap.right()
# act = expand_to_terms().left()
# eq @= {n:4}
# out = act.get_output_expression(eq)
# admap = act.get_addressmap(eq)

exp = x**2 | 1024
act = alg_pow_2_R()
admap = act.get_addressmap(exp)

None
