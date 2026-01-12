import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Algebra import *


class Quadratic(MetaExpression):
    def __init__(self, a, b, c, var=x):
        self.a = Smarten(a)
        self.b = Smarten(b)
        self.c = Smarten(c)
        Standard = a*x**2 + b*x + c
        f = lambda x: a*x**2 + b*x + c

        h = -b/(2*a)
        k = f(h)
        Vertex = a*(x-h)**2 + k

        D = b**2 - 4*a*c
        if D > 0:
            p = (-b + sqrt(D)) / (2*a)
            q = (-b - sqrt(D)) / (2*a)
            Factored = a*(x-p)*(x-q)
        elif D == 0:
            p = -b / (2*a)
            Factored = a*(x-p)**2
        elif D < 0:
            Factored = Expression()

        self.name_expression_dict = {
            'Standard':Standard,
            'Vertex':Vertex,
            'Factored':Factored
        }

