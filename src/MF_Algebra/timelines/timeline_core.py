from ..expressions import *
from ..actions import *
from MF_Tools.dual_compatibility import TransformMatchingTex, UP, smooth, Scene


class Timeline(MF_Base):
	def __init__(
		self,
		auto_color = {},
		auto_scale = 1,
		auto_fit = [None, None, None],
		auto_propagate = True,
		show_past_steps = False,
		past_steps_opacity = 0.4,
		past_steps_direction = UP,
		past_steps_buff = 1,
		past_steps_shift_run_time = 1,
		past_steps_shift_rate_func = smooth
	):
		self.steps = [] # Elements of this list are of the form [expression, action]
		self.current_exp_index = 0
		self.auto_color = auto_color
		self.auto_scale = auto_scale
		self.auto_fit = auto_fit
		self.auto_propagate = auto_propagate
		self.show_past_steps = show_past_steps
		if self.show_past_steps:
			self.past_steps_vgroup = VGroup()
			self.past_steps_opacity = past_steps_opacity
			self.past_steps_direction = past_steps_direction
			self.past_steps_buff = past_steps_buff
			self.past_steps_shift_run_time = past_steps_shift_run_time
			self.past_steps_shift_rate_func = past_steps_shift_rate_func

	def get_expression(self, index: int) -> Expression:
		try:
			return self.steps[index][0]
		except IndexError:
			return None

	def set_expression(self, index: int, expression: Expression):
		if self.auto_color:
			expression.set_color_by_subex(self.auto_color)
		if any(self.auto_fit):
			expression.mob.scale_to_fit(*self.auto_fit)
		elif self.auto_scale != 1:
			expression.mob.scale(self.auto_scale)
		if index == len(self.steps):
			self.add_expression_to_end(expression)
		self.steps[index][0] = expression
		if self.auto_propagate:
			self.propagate(start_at=index)

	def add_expression_to_start(self, expression: Expression):
		if len(self.steps) == 0 or self.steps[0][0] is not None:
			self.steps.insert(0, [None, None])
		self.set_expression(0, expression)
		return self

	def add_expression_to_end(self, expression: Expression):
		self.steps.append([None, None])
		self.set_expression(-1, expression)
		return self

	def get_action(self, index: int) -> Action:
		try:
			return self.steps[index][1]
		except IndexError:
			return None

	def set_action(self, index: int, action: Action):
		self.steps[index][1] = action
		if self.auto_propagate:
			self.propagate(start_at=index)

	def add_action_to_start(self, action: Action):
		self.set_action(0, action)
		return self

	def add_action_to_end(self, action: Action):
		if len(self.steps) == 0 or self.steps[-1][1] is not None:
			self.steps.append([None, None])
		self.set_action(-1,action)
		return self

	def propagate(self, start_at=0):
		for i in range(start_at, len(self.steps) - 1):
			exp, act = self.steps[i]
			next_exp = self.steps[i+1][0]
			if exp != None and act != None and next_exp == None:
				self.set_expression(i+1, act.get_output_expression(exp))
		exp, act = self.steps[-1]
		if exp != None and act != None:
			try:
				self.add_expression_to_end(act.get_output_expression(exp))
			except NotImplementedError:
				pass

	def get_addressmap(self, index):
		exp, act = self.steps[index]
		return act.get_addressmap(exp)

	def get_animation(self, index, **kwargs):
		action = self.get_action(index)
		expA = self.get_expression(index)
		expB = self.get_expression(index+1)
		if action:
			Animation = action.get_animation()(expA, expB, **kwargs)
		else:
			Animation = TransformMatchingTex(expA.mob, expB.mob, **kwargs)
		return Animation
	
	def next_animation(self, **kwargs):
		return self.get_animation(self.current_exp_index, **kwargs)

	def play_animation(self, scene, index, **kwargs):
		expA = self.get_expression(index)
		expB = self.get_expression(index+1)
		if self.show_past_steps:
			self.shift_past_steps(scene, expA, expB)
		animation = self.get_animation(index, **kwargs)
		scene.play(animation)
		self.current_exp_index = index+1

	def play_next(self, scene):
		self.play_animation(scene, index=self.current_exp_index)

	def play_range(self, scene, start_index, end_index, wait_between=1, **kwargs):
		for i in range(start_index, end_index):
			self.play_animation(scene, index=i, **kwargs)
			scene.wait(wait_between)

	def play_all(self, scene, wait_between=1, reset_exp_index=False):
		if reset_exp_index:
			self.current_exp_index = 0
		if self.mob not in scene.mobjects:
			scene.play(Write(self.mob))
		while self.current_exp_index < len(self.steps)-1:
			scene.wait(wait_between)
			self.play_next(scene=scene)

	def shift_past_steps(self, scene, expA, expB):
		mobA_radius = expA.mob.get_critical_point(self.past_steps_direction) - expA.mob.get_center()
		mobB_radius = expB.mob.get_center() - expB.mob.get_critical_point(-self.past_steps_direction)
		shift_distance = np.linalg.norm(mobA_radius) + np.linalg.norm(mobB_radius) + self.past_steps_buff
		self.past_steps_vgroup.add(
			self.mob.copy().set_opacity(0.25)
		)
		scene.add(self.past_steps_vgroup)
		scene.play(
			self.past_steps_vgroup.animate.shift(shift_distance * self.past_steps_direction),
			run_time = self.past_steps_shift_run_time,
			rate_func = self.past_steps_shift_rate_func
		)

	def __repr__(self):
		return f"Timeline({str([[repr(exp), repr(act)] for exp, act in self.steps])})"

	def get_vgroup(self, **kwargs):
		return VGroup(*[self.steps[i][0].mob for i in range(len(self.steps))])
	
	@property
	def vgroup(self):
		return self.get_vgroup()

	@property
	def mob(self):
		return self.exp.mob

	@property
	def exp(self):
		return self.expressions[self.current_exp_index]

	@property
	def expressions(self):
		return [exp for exp,act in self.steps]

	@property
	def actions(self):
		return [act for exp,act in self.steps]

	def reset(self, reset_caches=True):
		self.current_exp_index = 0
		if reset_caches:
			for exp in self.expressions:
				exp.reset_caches()

	def undo_last_action(self):
		if self.actions[-1] is not None:
			self.steps[-1] = [self.steps[-1][0], None]
		else:
			self.steps.pop()
			self.undo_last_action()

	def reset_caches(self):
		for i,exp in enumerate(self.expressions):
			exp.reset_caches()
			self.set_expression(i, exp)

	def align_on_equals(self, strength=1):
		self.get_vgroup()
		equals_positions = [exp['='].get_center() for exp in self.expressions]
		avg = np.mean(np.stack(equals_positions), axis=0)
		for exp, pos in zip(self.expressions, equals_positions):
			exp.mob.shift(strength*(avg - pos))
		return self

	def get_mob_ladder(self):
		from MF_Tools.dual_compatibility import VGroup, ArcBetweenPoints, RIGHT, Text, ORANGE
		ladder = VGroup()
		mobs = self.get_vgroup().copy()
		ladder.expressions = mobs.arrange(DOWN, buff=1)
		ladder.arrows = VGroup(*[
			ArcBetweenPoints(
				np.array([mobs.get_edge_center(RIGHT)[0], m1.get_center()[1]-0.1, 0]),
				np.array([mobs.get_edge_center(RIGHT)[0], m2.get_center()[1]+0.1, 0]),
				angle=-3/4*PI
			).shift(0.75*RIGHT).set_stroke(width=2, opacity=0.5)
			for m1, m2 in zip(mobs[:-1], mobs[1:])
		])
		ladder.actions = VGroup(*[
			Text(repr(act)).scale(0.6).next_to(arrow, RIGHT, buff=0.25)
			for act, arrow in zip(self.actions, ladder.arrows)
		])
		ladder.addressmaps = VGroup(*[
			VGroup(*[
				Text(str(entry)).set_color(ORANGE)
				for entry in addressmap
			]).arrange(DOWN).scale(0.25).next_to(ladder.actions[i], DOWN)
			for i, addressmap in enumerate([
				act.get_addressmap(exp)
				for exp, act in zip(self.expressions[:-1], self.actions)
			])
		])
		ladder.add(ladder.expressions, ladder.arrows, ladder.actions, ladder.addressmaps)
		return ladder
	
	def save_to_file(self, filename):
		from ..utils import save_to_file
		for exp in self.expressions:
			exp._mob = None
		save_to_file(self, filename)

	def debug_anim(self, scene, i):
		scene.remove(self.mob)
		exp, act = self.steps[i]
		print('Input expression:', exp)
		print('Output expression:', act.get_output_expression(exp))
		print('Addressmap:')
		for entry in act.get_addressmap(exp):
			print(entry)
		self.play_animation(scene, i)

	def __le__(self, expr):
		assert isinstance(expr, Expression), "Can only apply expression >= timeline"
		for act in self.actions:
			expr = act <= expr
		return expr



class TimelineScene(Scene):
	def __init__(self, *args, **kwargs):
		self.timeline = Timeline()
		super().__init__(*args, **kwargs)

	def add_and_play(self, action):
		self.timeline >> action
		self.timeline.play_all(self)

	def __and__(self, action):
		self.add_and_play(action)
		return self

	def suspend(self):
		self.timeline.suspend()

	def resume(self):
		self.timeline.resume()
	
	def add_ladder(self):
		self.ladder = self.timeline.get_mob_ladder()
		self.ladder.scale_to_fit(4, 8).center()
		self.clear()





