
# Needed because {**A, **B} does not work in MicroPython
def merge_dicts(*dicts):
	result = {}
	for D in dicts:
		result |= D
	return result


# Needed because [*A, *B] does not work in MicroPython
def merge_lists(*lists):
	result = []
	for L in lists:
		result += L
	return result
