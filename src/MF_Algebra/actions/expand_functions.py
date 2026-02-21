from .action_core import Action, IncompatibleExpression
from ..expressions.functions import Function, ApplyFunction, BigOperator


class expand_to_terms(Action):
    def get_output_expression(self, input_expression):
        assert isinstance(input_expression, ApplyFunction)
        operator, arg = input_expression.children
        assert isinstance(operator, BigOperator)
        terms = operator.expand_on_args(arg)
        return terms

    def get_addressmap(self, input_expression, **kwargs):
        out_expr = self.get_output_expression(input_expression)
        print('Admap In Exp: ', input_expression)
        print('Admap Out Exp: ', out_expr)
        admap = []
        for j in range(len(out_expr.children)):
            admap.append(['1', f'{j}', {'path_arc':2}]) # not working right on many children
        admap.append(['0', '+', {'path_arc':-2, 'run_time':1.25}])
        return admap


class apply_func_rule(Action):
    def get_output_expression(self, input_expression):
        assert isinstance(input_expression, ApplyFunction)
        return input_expression.expand_on_args()

    def get_addressmap(self, input_expression, **kwargs):
        pass # This needs glyphmap I think?


