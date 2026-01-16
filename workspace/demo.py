import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *




algebra_config['multiplication_mode'] = 'dot'
class Demo_Evaluate(Scene):
    def construct(self):
        exp = 3*x**2-(4+x)/sqrt(y-1)
        E = Evaluate(exp, auto_color={x:RED, y:BLUE})
        E >> substitute_({x:8, y:10}, maintain_color=True)
        E.play_all(self)
        self.embed()









class Demo_Solve(Scene):
    def construct(self):
        eq = 13/(x+8)**2+5 | 10
        T = Solve(x, eq)
        T.play_all(self)
        self.embed()



algebra_config['always_color'] = {x:RED, y:BLUE, z:GREEN}
class Demo_Solve_2(Scene):
    def construct(self):
        eq = a*x + b*5**y | c*z*y
        T = Solve(solve_for=y, show_past_steps=True)
        T >> eq
        T.play_all(self)
        self.embed()



