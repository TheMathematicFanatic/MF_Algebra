

def apply_addressmap(address:str, addressmap:list, reverse:bool=False) -> set:
	"""    
	Turns one address into another (or several), according to an addressmap.
	If it is explicitly listed in the addressmap, it simply returns the address on the other side.
	If it is not listed, it checks all the entries with that address as a prefix, and outputs the corresponding prefix on the other side.
	It also checks if any entry is a prefix of the address, in which cases it replaces that section of the address with the corresponding prefix.
	It may be found multiple times or not at all, which is why it returns a set. I think that makes sense but I'm not sure.
	The output set can have any number, you usually are expecting a singleton, empty or multiple usually means failure.
	Reverse simply goes from right to left across the addressmap instead of left to right.
	Returns None if address is ever mapped to [], meaning that subex is meant to fade in or out.
	
	Examples:
	>>> apply_addressmap('12', [['123', '999']])
	{'99'}
	>>> apply_addressmap('123', [['12', '88'], ['1', '5']])
	{'883', '523'}
	>>> apply_addressmap('12', [['1', []]])
	None
	"""

	la = len(address)
	from_ads = [entry[int(reverse)] for entry in addressmap]
	to_ads = [entry[int(not reverse)] for entry in addressmap]
	results = set()

	for from_ad, to_ad in zip(from_ads, to_ads):
		if isinstance(from_ad, type) or isinstance(to_ad, type):
			# Address is being explicitly animated in or out
			return None

		lf,lt = len(from_ad), len(to_ad)

		# Case 1: address is equal to from_ad or some prefix of it
		if address == from_ad[:la]:
			if to_ad == []: return None
			results.add(to_ad[:la-lf or None])

		# Case 2: from_ad is a prefix of address
		elif from_ad == address[:lf]:
			if to_ad == []: return None
			results.add(to_ad + address[lf:])

	return results