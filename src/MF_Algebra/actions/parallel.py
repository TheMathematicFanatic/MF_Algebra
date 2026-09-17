from .action_core import Action


class ParallelAction(Action):
	def __init__(self, *actions, lag=0, **kwargs):
		self.actions = list(actions)
		self.lag = lag
		super().__init__(**kwargs)
	
	def get_output_expression(self, input_expression=None):
		expr = input_expression
		for action in self.actions:
			expr = action.get_output_expression(expr)
		return expr
	
	get_addressmap_decorators = ( # This application proves that this is a great architecture!
		Action.preaddressmap, # This one is needed so that if the parallel has an additional pread it can be applied,
		# Action.autoparenmap, # But these two are not needed because they're already handled by the constituents... I think?
		# Action.autoopmap, # Actually I think I can imagine some crazy cases where this isn't quite sufficient.... ughhh
		# Action.autokwargmap, # Idek about this guy
	)
	def get_addressmap(self, input_expression=None):
		total_addressmap = []
		for i,act in enumerate(self.actions):
			for entry in act.get_addressmap(input_expression):
				if len(entry) == 2: entry.append({})
				entry[2]['delay'] = entry[2].get('delay', 0) + i*self.lag
				total_addressmap.append(entry)
		return total_addressmap

	def __or__(self, other):
		if isinstance(other, ParallelAction):
			return ParallelAction(*self.actions, *other.actions)
		elif isinstance(other, Action):
			return ParallelAction(*self.actions, other)
		else:
			raise ValueError("Can only use | with other ParallelAction or Action")
	
	def __ror__(self, other):
		if isinstance(other, Action):
			return ParallelAction(other, *self.actions)
		else:
			return NotImplemented


