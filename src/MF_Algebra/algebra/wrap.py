from .algebra_core import AlgebraicAction
from ..expressions import Expression

#TODO I did not finish what I was doing here but I gotta commit changes and I gotta go to bed

class rewrap_subex_(AlgebraicAction):
	auto_morph = True
	auto_resolve_kwargs = {'path_arc':1, 'lag_ratio':0.03, 'delay':0.25}
	def __init__(self,
		start_exp:Expression = None,
		end_exp:Expression = None,
		target_subex:Expression = None,
		**kwargs
	):
		self.start_exp = start_exp
		self.end_exp = end_exp
		self.target_subex = target_subex
		self.start_ads = start_exp.get_addresses_of_subex(target_subex)
		self.end_ads = end_exp.get_addresses_of_subex(target_subex)
		super().__init__(self.start_exp, self.end_exp, **kwargs)
	
	def get_addressmap(self, input_expression=None):
		if len(self.start_ads) == len(self.end_ads):
			return [
				[start_ad, end_ad]
				for start_ad, end_ad in zip(self.start_ads, self.end_ads)
			]
		else:
			return [
				[start_ad, end_ad]
				for start_ad in self.start_ads for end_ad in self.end_ads
			]




class unwrap_subex_(rewrap_subex_):
	def __init__(self,
		outer_exp,
		target_subex,
		**kwargs
	):
		super().__init__(
			start_exp = outer_exp,
			end_exp = target_subex,
			target_subex = target_subex,
			**kwargs
		)



from ..actions import Action
class unwrap_subex_(Action):
	def __init__(self, address, **kwargs):
		self.address = address
		super().__init__(**kwargs)
	
	def get_output_expression(self, input_expression):
		return input_expression.get_subex(self.address)
	
	def get_addressmap(self, input_expression, **kwargs):
		return [
			[self.address, ''],
			['!'+self.address, []]
		]