from ...expressions.functions.functions import *
from ...expressions.variables import Variable
import numpy as np


theta = Variable("\\theta")

sin = Function("\\sin", 3, python_rule=np.sin, parentheses_mode="weak")
cos = Function("\\cos", 3, python_rule=np.cos, parentheses_mode="weak")
tan = Function("\\tan", 3, python_rule=np.tan, parentheses_mode="weak")
cot = Function("\\cot", 3, python_rule=lambda x: 1/np.tan(x), parentheses_mode="weak")
sec = Function("\\sec", 3, python_rule=lambda x: 1/np.cos(x), parentheses_mode="weak")
csc = Function("\\csc", 3, python_rule=lambda x: 1/np.sin(x), parentheses_mode="weak")

