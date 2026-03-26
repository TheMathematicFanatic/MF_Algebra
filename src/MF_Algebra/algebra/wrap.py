from .algebra_core import AlgebraicAction
from ..expressions import Expression



class rewrap_subex_(AlgebraicAction):
	def __init__(self,
		start_exp:Expression = None,
		end_exp:Expression = None,
		target_subex:Expression = None,
		**kwargs
	):
		self.target_subex = target_subex
		self.start_exp = start_exp
		self.end_exp = end_exp
		start_ads = start_exp.get_addresses_of_subex(target_subex)
		end_ads = end_exp.get_addresses_of_subex(target_subex)
		assert len(start_ads) == len(end_ads) == 1, 'Target subexpression must be unique in both expressions.'
		# I'd love to make it work for several but I don't know how to get all glyphs except for more than one subexpression in an addressmap
		self.start_ad = start_ads[0]
		self.end_ad = end_ads[0]
		super().__init__(self.start_exp, self.end_exp, **kwargs)
	
	def get_addressmap(self, input_expression=None):
		return [
			[self.start_ad, self.end_ad, {'delay':0.25}],
			['!'+self.start_ad, '!'+self.end_ad, {'path_arc':3}],
		]


class wrap_subex_(rewrap_subex_):
	def __init__(self,
		outer_exp,
		**kwargs
	):
		super().__init__(
			start_exp = outer_exp,
			end_exp = None,
			target_subex = None,
			**kwargs
		)
	



# class unwrap_subex_(rewrap_subex_):
# 	def __init__(self,
# 		outer_exp,
# 		target_subex,
# 		**kwargs
# 	):
# 		super().__init__(
# 			start_exp = outer_exp,
# 			end_exp = target_subex,
# 			target_subex = target_subex,
# 			**kwargs
# 		)

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