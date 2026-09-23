from ..actions import Action, IncompatibleExpression
from ..expressions import Expression
from . import AutoTimeline


class TimeWeb:
	def __init__(self, starting_expression):
		current_hash = hash(starting_expression)
		self.web = {
			# hash : [Expression, {(Action, to_hash), ...}, { (Action, from_hash), ...} ]
			current_hash : [starting_expression, set(), set() ]
		}
		self.current_hash = current_hash
	
	def __getitem__(self, key):
		if isinstance(key, Expression):
			return self.web[hash(key)]
		super().__getitem__(key)
	
	def __setitem___(self, key):
		hash_val = hash(key)
		if hash_val not in self.web:
			self.add_new_expression(key)
		return self.web[hash_val]
	
	def __contains__(self, item):
		if isinstance(item, Expression):
			return hash(item) in self.web
		super().__getitem__(item)
	
	@property
	def current_expression(self):
		return self.web[self.current_hash][0]
	
	@property
	def outgoing_actions(self):
		return self.web[self.current_hash][1]
	
	@property
	def incoming_actions(self):
		return self.web[self.current_hash][2]
	
	@property
	def expressions(self):
		return {val[0] for val in self.web.values()}
	
	def expression_from_hash(self, key):
		return self.web[key][0]
	
	def add_new_expression(self, expression):
		if not expression in self:
			self.web[hash(expression)] = [expression, set(), set()]
		return self

	def add_new_action(self, action, in_exp=None, out_exp=None, change_current=True, ignore_exception=True):
		if in_exp is None:
			in_exp = self.current_expression
		in_hash = hash(in_exp)
		if out_exp is None:
			try:
				out_exp = action.get_output_expression(in_exp)
			except IncompatibleExpression:
				if ignore_exception:
					return self
				else:
					raise IncompatibleExpression
		out_hash = hash(out_exp)
		self.add_new_expression(out_exp)
		self[in_exp][1].add((action, out_hash))
		self[out_exp][2].add((action, in_hash))
		if change_current:
			self.current_hash = out_hash
		return self

	def __rshift__(self, act):
		return self.add_new_action(act)

	def generate_all(self, *actions, at_all_preaddresses=False, at_twig_preaddresses=False, bailsize=None):
		# Not guaranteed to terminate!!!
		touched_expressions = set()
		untouched_expressions = self.expressions
		while untouched_expressions and (bailsize is None or len(untouched_expressions) < bailsize):
			for exp in untouched_expressions:
				if at_all_preaddresses:
					preaddresses = exp.get_all_nonleaf_addresses()
				elif at_twig_preaddresses:
					preaddresses = exp.get_all_twig_addresses()
				else:
					preaddresses = ['']
				for act in actions:
					for ad in preaddresses:
						self.add_new_action(act.pread(ad), exp, change_current=False, ignore_exception=True)
				touched_expressions.add(exp)
			untouched_expressions = self.expressions - touched_expressions
		return self
	
	def generate_evaluate(self):
		from ..actions.evaluation import evaluate_
		return self.generate_all(evaluate_(), at_twig_preaddresses=True)
	
	def generate_algebra_maneuvers(self):
		from ..algebra.equations import EquationManeuver
		return self.generate_all(*EquationManeuver.all_actions())
	
	def generate_from_timelines(self, *timelines, additional_actions=[], **kwargs):
		# Not guaranteed to terminate!!!
		touched_expressions = set()
		untouched_expressions = self.expressions
		while untouched_expressions:
			for exp in untouched_expressions:
				for TimelineClass in timelines:
					T = TimelineClass().suspend().add_expression_to_start(exp)
					act = T.decide_next_action(0)
					if act:
						self.add_new_action(act, exp, change_current=False, ignore_exception=True)
				for act in additional_actions:
					self.add_new_action(act, exp, change_current=False, ignore_exception=True)
				touched_expressions.add(exp)
			untouched_expressions = self.expressions - touched_expressions
		return self
	
	def reset_caches(self):
		for exp in self.expressions:
			exp.reset_caches()
		return self


	def get_universal_json(self):
		json = {
			'expressions' : {},  # exp_hash : {'latex':texstr, 'xml':svgstr} 
			'actions'     : {},  # act_hash : {'action':classname, 'label':divide by 3, 'from_exp':hash, 'to_exp':hash, 'preaddress':preaddress, 'glyphmap':uvgm}
			'graph'       : {},  # exp_hash : {'outgoing': [(act_hash,exp_hash),...], 'incoming': [(act_hash,exp_hash),...]}
		}
		for exp_hash, (exp, outgoing, incoming) in self.web.items():
			latex = str(exp) # convert Expression to latex string
			xml = exp.mob.get_svg_string()
			json['expressions'][exp_hash] = {
				'latex':latex,
				'xml':xml
			}
			json['graph'][exp_hash] = {'outgoing':[], 'incoming':[]}
			for act, out_hash in outgoing:
				act_hash = int(str(hash((act, exp_hash, out_hash)))[:15])
				uvg = act.get_universal_glyphmap(exp)
				label = act.get_label()
				json['actions'][act_hash] = {
					'action'         : act.__class__.__name__,
					'label'          : label,
					'from_exp'       : exp_hash,
					'to_exp'         : out_hash,
					'glyphmap'       : uvg,
				}
				json['graph'][exp_hash]['outgoing'].append((act_hash, out_hash))
			for act, in_hash in incoming:
				act_hash = int(str(hash((act, exp_hash, out_hash)))[:15])
				json['graph'][exp_hash]['incoming'].append((act_hash, in_hash))
		return json



class TimeWeb2:
	def __init__(self, starting_expression=None):
		self.expressions = {} # hash_exp : expression
		self.actions = {} # hash_act : (action, in_exp, out_exp, glyphmap)
		self.connections = {} # hash_exp : [act_hashes]
		if starting_expression is not None:
			self.add_expression(starting_expression)
	
	def add_expression(self, expression):
		hash_exp = hash(expression)
		self.expressions[hash_exp] = expression
	
	def add_action(self, action:Action, in_exp):
		hash_exp = hash(in_exp)
		assert hash_exp in self.expressions
		out_exp = action.get_output_expression(in_exp)
		self.add_expression(out_exp)
		addressmap = action.get_addressmap(in_exp)
		glyphmap = action.get_glyphmap(in_exp, out_exp, addressmap)
		hash_act = hash((action, in_exp, out_exp))
		self.actions[hash_act] = (action, in_exp, out_exp, glyphmap)
		# self.connections[hash_exp]





