import pytest
import sys
sys.argv = ['MF_Algebra'] # Necessary because otherwise manimgl tries to parse pytest cli args as its own
from MF_Algebra import *
from copy import deepcopy



def MFparam(arg_names, list_of_id_inputs_expectation):
	return pytest.mark.parametrize(
		arg_names, # such as 'expr, address, subex'
		[
			pytest.param(*map(deepcopy, inputs), output, id=id)
			for id, *inputs, output in list_of_id_inputs_expectation
		]
	)

