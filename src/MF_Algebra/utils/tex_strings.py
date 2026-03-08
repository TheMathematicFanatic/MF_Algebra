

def add_spaces_around_brackets(input_string:str) -> str:
	# Needed so that Manim does not apply its special interpretation of double brackets
	result = []
	i = 0
	length = len(input_string)

	for i in range(length):
		if input_string[i:i+2] == '{{':
			result.append('{ ')
		elif input_string[i:i+2] == '}}':
			result.append('} ')
		else:
			result.append(input_string[i])

	# Join the list into a single string and remove any extra spaces
	return ''.join(result).strip()


