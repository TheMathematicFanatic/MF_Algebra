from sympy import Expr, E, symbols
from sympy.parsing.latex import parse_latex
import re
import asteval



def MF_Algebra_to_sympy(exp):
	latex = str(exp)
	sympy_expr = parse_latex(latex)

	# Special case substitution needed so that e is interpreted as the constant and not a variable
	sympy_expr = sympy_expr.subs(symbols('e'), E)

	return sympy_expr



def text_to_MF_Algebra(text):
	# Token regex
	token_re = re.compile(
		r"""
		(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)   # numbers
		| [a-zA-Z_]\w*                     # identifiers
		| \^                                # caret
		| =                                 # equals
		| [()+\-*/]                         # operators and parentheses
		""",
		re.VERBOSE
	)

	# Helper to categorize tokens
	def categorize(tok):
		if tok in '+-*/()**':
			return 'op'
		if tok == '**':
			return 'caret'
		if tok == '|':
			return 'equals'
		if re.match(r'(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)$', tok):
			return 'number'
		return 'identifier'

	def rewrite_expression(s):
		# Step 1: tokenize & replace numbers/operators
		raw_tokens = token_re.findall(s)
		tokens = []
		for tok in raw_tokens:
			if tok == '^':
				tokens.append('**')
			elif tok == '=':
				tokens.append('|')
			elif re.match(r'(?<!\w)-?(?:\d+\.\d*|\.\d+|\d+)$', tok):
				tokens.append(f"Real({tok})" if '.' in tok else f"Integer({tok})")
			else:
				tokens.append(tok)

		# Step 2: insert implicit multiplication
		result = [tokens[0]]
		for prev, curr in zip(tokens, tokens[1:]):
			prev_cat = categorize(prev)
			curr_cat = categorize(curr)
			
			# new rules for implicit multiplication
			if ((prev_cat in ('number', 'identifier') or prev == ')') and
				(curr_cat in ('number', 'identifier') or curr == '(')):
				result.append('*')
			result.append(curr)
		return ''.join(result)

	from MF_Algebra import Integer, Real, Variable, Function, sqrt, cbrt, sin, cos, tan, csc, sec, cot
	symtable = {
		**{L: Variable(L, 1) for L in 'abcjklmnopqrstuvwxyz'},
		**{F: Function(F, 1) for F in 'fgh'},
		'Integer' : Integer,
		'Real' : Real,
		'Variable' : Variable,
		'sqrt' : sqrt,
		'cbrt' : cbrt,
		'sin' : sin,
		'cos' : cos,
		'tan' : tan,
		'csc' : csc,
		'sec' : sec,
		'cot' : cot,
	}
	aeval = asteval.Interpreter(symtable=symtable)

	return aeval(rewrite_expression(text))


