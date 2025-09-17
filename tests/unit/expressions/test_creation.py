from conftest import *


def test_create_Variable():
	Variable('V')

def test_create_Integer():
	Integer(-120)

def test_create_Real():
	Real(-0.6180339887498949)

def test_create_add():
	Add(Integer(1), Integer(2))

def test_create_sub():
	Sub(Integer(1), Integer(2))

def test_create_mul():
	Mul(Integer(1), Integer(2))

def test_create_div():
	Div(Integer(1), Integer(2))

def test_create_pow():
	Pow(Integer(1), Integer(2))

def test_create_sequence():
	Sequence(Integer(1), Integer(2))

def test_create_equation():
	Equation(Integer(1), Integer(2))

def test_create_function():
	Function('f')
