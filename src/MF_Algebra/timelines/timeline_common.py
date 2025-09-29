from .timeline_core import *
from .timeline_variants import *
from ..expressions.variables import Variable


class Evaluate(AutoTimeline):
	def __init__(self, first_expression=None, mode="one at a time", number_mode="float", **kwargs):
		self.mode = mode
		self.number_mode = number_mode
		super().__init__(**kwargs)
		if first_expression is not None:
			self.add_expression_to_start(first_expression)

	def decide_next_action(self, index: int):
		last_exp = self.get_expression(index)
		leaves = last_exp.get_all_leaf_addresses()
		if leaves == ['']:
			return None
		leaves.sort(key=len, reverse=True)
		for leaf in leaves:
			try:
				from ..actions.evaluation import evaluate_
				twig = leaf[:-1]
				action = evaluate_(preaddress=twig)
				action.get_output_expression(last_exp)
				return action
			except ValueError:
				# This should mean that a subexpression cannot be computed due to the presence of a variable.
				# Perhaps we should make a custom Exception class for this so as not to accidentally catch others.
				pass
		return None



class Solve(AutoTimeline):
	def __init__(self, solve_for=Variable('x'), first_expression=None, preferred_side=None, auto_evaluate=True, **kwargs):
		super().__init__(**kwargs)
		if first_expression is not None:
			self.add_expression_to_start(first_expression)
		self.solve_for = solve_for
		self.auto_evaluate = auto_evaluate
		self.all_actions_to_try = []
		from ..actions.algebra.equations import EquationManeuver
		for maneuver_ in EquationManeuver.__subclasses__():
			self.all_actions_to_try += [
				maneuver_(),
				maneuver_().reverse(),
				maneuver_().flip(),
				maneuver_().reverse_flip()
			]
	
	def decide_next_action(self, index:int):
		last_exp = self.get_expression(index)
		current_addresses = last_exp.get_addresses_of_subex(self.solve_for)
		assert len(current_addresses)==1, f"I don't know what to do if variable appears {len(current_addresses)} times"
		current_address = current_addresses[0]

		if self.auto_evaluate:
			try:
				result = (Evaluate(last_exp)).decide_next_action(0)
				if result is not None:
					return result
			except:
				pass

		if current_address == '1':
			return swap_children_()
		if current_address == '0':
			return None

		if self.solve_for is not None:
			successful_outputs = []
			for maneuver in self.all_actions_to_try:
				try:
					next_exp = maneuver.get_output_expression(last_exp)
					new_address = next_exp.get_addresses_of_subex(self.solve_for)[0]
					successful_outputs.append((maneuver, new_address))
				except:
					pass
			
			if len(successful_outputs) == 0:
				return None
			shortest_result = min(successful_outputs, key=lambda p: len(p[1]))
			assert len(shortest_result[1]) <= len(current_address)
			return shortest_result[0]

		return None

	def set_solve_for(self, var):
		self.solve_for = var
		self.resume()


class EvaluateAndSolve(CombinedRuleTimeline):
	def __init__(self, *args, **kwargs):
		super().__init__(Evaluate, Solve, *args, **kwargs)


class SolveAndEvaluate(Solve, Evaluate):
	def __init__(self, *args, **kwargs):
		Solve.__init__(self, *args, **kwargs)
		Evaluate.__init__(self, *args, **kwargs)
	
	def decide_next_action(self, index):
		return super().decide_next_action(index)
