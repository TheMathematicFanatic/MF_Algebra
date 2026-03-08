from abc import ABC
from dataclasses import dataclass
from copy import deepcopy
from .type_fixing import Smarten


@dataclass
class MF_Base(ABC):
	def copy(self):
		return deepcopy(self)

	def __rshift__(self, other):
		other = Smarten(other)
		return combine_to_timeline(self, other)

	def __rrshift__(self, other):
		other = Smarten(other)
		return other.__rshift__(self)

	def __eq__(self, other):
		other = Smarten(other)
		if type(self) != type(other):
			return False
		else:
			return self.hash_key() == other.hash_key()

	def __hash__(self):
		return hash(self.hash_key())

	def hash_key(self):
		raise NotImplementedError


def combine_to_timeline(A, B):
	from ..expressions.expression_core import Expression
	from ..actions.action_core import Action
	from ..timelines.timeline_core import Timeline
	if isinstance(A, Expression) and isinstance(B, Expression):
		return Timeline().add_expression_to_start(A).add_expression_to_end(B)
	elif isinstance(A, Expression) and isinstance(B, Action):
		return Timeline().add_expression_to_start(A).add_action_to_end(B)
	elif isinstance(A, Action) and isinstance(B, Expression):
		return Timeline().add_action_to_start(A).add_expression_to_end(B)
	elif isinstance(A, Action) and isinstance(B, Action):
		return Timeline().add_action_to_start(A).add_action_to_end(B)
	elif isinstance(A, Expression) and isinstance(B, Timeline):
		return B.add_expression_to_start(A)
	elif isinstance(A, Action) and isinstance(B, Timeline):
		return B.add_action_to_start(A)
	elif isinstance(A, Timeline) and isinstance(B, Expression):
		return A.add_expression_to_end(B)
	elif isinstance(A, Timeline) and isinstance(B, Action):
		return A.add_action_to_end(B)
	elif isinstance(A, Timeline) and isinstance(B, Timeline):
		return A.combine_timelines(B) #TODO
	else:
		raise NotImplementedError(f"Unsupported combination of types {type(A)} and {type(B)}")
