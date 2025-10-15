from .action_core import Action


class ParallelAction(Action):
    def __init__(self, *actions, **kwargs):
        self.actions = list(actions)
        super().__init__(**kwargs)
    
    @Action.preaddressfunc
    def get_output_expression(self, input_expression=None):
        expr = input_expression
        for action in self.actions:
            expr = action.get_output_expression(expr)
        return expr

    @Action.autoparenmap
    @Action.preaddressmap
    def get_addressmap(self, input_expression=None):
        return sum([action.get_addressmap(input_expression) for action in self.actions], [])
    
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


