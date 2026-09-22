import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from manimlib import *
from MF_Algebra import *


import time
start = time.perf_counter()

D = Differentiate()
D >> d(a**6+b**9+sin(z**3))
print(D.steps)

print(f"took {time.perf_counter() - start:.3f}s")