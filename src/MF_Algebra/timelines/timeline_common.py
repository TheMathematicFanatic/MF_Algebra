from .timeline_core import *
from .timeline_variants import *
from ..expressions.variables import Variable
from ..actions.evaluation import evaluate_
from ..expressions.combiners.relations import Relation


class Evaluate(AutoTimeline):
	def __init__(self, first_expression=None, mode="one at a time", number_mode="float", **kwargs):
		self.mode = mode
		self.number_mode = number_mode
		super().__init__(**kwargs)
		if first_expression is not None:
			self.add_expression_to_start(first_expression)

	def decide_next_action(self, index: int):
		last_exp = self.get_expression(index)
		twig_ads = last_exp.get_all_twig_addresses()
		for twig_ad in twig_ads:
			if not isinstance(last_exp.get_subex(twig_ad), Relation):
				try:
					action = evaluate_().pread(twig_ad)
					action.get_output_expression(last_exp)
					return action
				except (ValueError, IncompatibleExpression):
					pass
		return None



class Solve(AutoTimeline):
	def __init__(self, solve_for=None, first_expression=None, preferred_side=None, auto_evaluate=True, **kwargs):
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
		if self.solve_for is None:
			self.solve_for = last_exp.get_all_variables().pop()
		current_addresses = last_exp.get_addresses_of_subex(self.solve_for)
		assert len(current_addresses)==1, f"I don't know what to do if variable appears {len(current_addresses)} times"
		current_address = current_addresses[0]

		if self.auto_evaluate:
			try:
				result = (Evaluate(last_exp)).decide_next_action(0)
				if result is not None:
					return result
			except IncompatibleExpression:
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
				except IncompatibleExpression:
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
