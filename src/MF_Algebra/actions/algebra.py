from .action_core import *
from ..expressions.expression_common import *
from MF_Tools.dual_compatibility import PI, FadeIn, FadeOut, Write, Uncreate
from .action_common import swap_children_


class AlgebraicAction(Action):
    def __init__(self, template1, template2, var_kwarg_dict={}, extra_addressmaps=[], **kwargs):
        super().__init__(**kwargs)
        self.template1 = template1
        self.template2 = template2
        self.var_kwarg_dict = var_kwarg_dict #{a:{"path_arc":PI}}
        self.extra_addressmaps = extra_addressmaps
        self.addressmap = None
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        var_dict = match_expressions(self.template1, input_expression)
        return self.template2.substitute(var_dict)
    
    @preaddressmap
    def get_addressmap(self, input_expression=None):
        # Best overwritten in subclasses, but this gets the job done sometimes.
        # Actually, I think most subclasses will have a static addressmap, so I'll add this line at the start.
        if self.addressmap is not None:
            return self.addressmap

        addressmap = []
        def get_var_ad_dict(template):
            template_leaves = {
                template.get_subex(ad)
                for ad in template.get_all_leaf_addresses()
                }
            from ..expressions.variables import Variable
            variables = [var for var in template_leaves if isinstance(var, Variable)]
            return {var: template.get_addresses_of_subex(var) for var in variables}
        self.template1_address_dict = get_var_ad_dict(self.template1)
        self.template2_address_dict = get_var_ad_dict(self.template2)
        variables = self.template1_address_dict.keys() | self.template2_address_dict.keys()
        for var in variables:
            kwargs = self.var_kwarg_dict.get(var, {})
            if len(self.template1_address_dict[var]) == 1:
                addressmap += [[self.template1_address_dict[var][0], t2ad, kwargs] for t2ad in self.template2_address_dict[var]]
            elif len(self.template2_address_dict[var]) == 1:
                addressmap += [[t1ad, self.template2_address_dict[var][0], kwargs] for t1ad in self.template1_address_dict[var]]
            else:
                raise ValueError("I don't know what to do when a variable appears more than once on both sides. Please set addressmap manually.")
        addressmap += self.extra_addressmaps
        return addressmap

    def __repr__(self):
        return f"AlgebraicAction({self.template1}, {self.template2})"
    
    # def get_animation(self, *args, **kwargs):
    #     return super().get_animation(*args, auto_fade=True, auto_resolve_delay=0.1, **kwargs)

    def reverse(self):
        # swaps input and output templates
        self.template1, self.template2 = self.template2, self.template1


class EquationManeuver(AlgebraicAction):
    # Watch out, these cannot be preaddressed currently.
    # But I can't conceive of why you'd want to do that anyway.
    # Perhaps for a sequence of equations?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def reverse(self):
        # swaps input and output templates
        self.template1, self.template2 = self.template2, self.template1
        # modifies addressmap accordingly
        # (swap order and negate path_arcs)
        for entry in self.addressmap:
            entry[0], entry[1] = entry[1], entry[0]
            if len(entry) == 3 and 'path_arc' in entry[2].keys():
                entry[2]['path_arc'] = -entry[2]['path_arc']
        return self

    def flip(self):
        # flips the equations of both templates
        s = swap_children_()
        self.template1 = s.get_output_expression(self.template1)
        self.template2 = s.get_output_expression(self.template2)
        # modifies addressmap accordingly
        # (swap first character of addresses and negate path_arcs)
        for entry in self.addressmap:
            if isinstance(entry[0], str):
                entry[0] = str(1-int(entry[0][0])) + entry[0][1:]
            if isinstance(entry[1], str):
                entry[1] = str(1-int(entry[1][0])) + entry[1][1:]
            if len(entry) == 3 and 'path_arc' in entry[2].keys():
                entry[2]['path_arc'] = -entry[2]['path_arc']
        return self

    def reverse_flip(self):
        return self.reverse().flip()
    
    






class alg_add_R(EquationManeuver):
    def __init__(self, **kwargs):
        super().__init__(
            a + b & c,
            a & c - b,
            **kwargs
        )
        self.addressmap = (
            ['01', '11', {'path_arc':PI}],
            ['0+', '1-', {'path_arc':PI}],
        )


class alg_add_L(EquationManeuver):
    def __init__(self, **kwargs):
        super().__init__(
            a + b & c,
            b & c - a,
            **kwargs
        )
        self.addressmap = (
            ['00', '11', {'path_arc':PI}],
            ['0+', '1-', {'path_arc':PI}]
        )
        # return (
        #     ['00', '11', {'path_arc':PI}],
        #     ['0+', FadeOut, {'run_time':0.5}],
        #     [FadeIn, '1-', {'run_time':0.5, 'delay':0.5}]
        # )


class alg_mul_R(EquationManeuver):
    def __init__(self, **kwargs):
        super().__init__(
            a * b & c,
            a & c / b,
            **kwargs
        )
        self.addressmap = (
            ['01', '11', {'path_arc':PI}],
            #['0*', FadeOut, {'run_time':0.5}],
            [Write, '1/', {'run_time':0.5, 'delay':0.5}]
        )
    
    def reverse(self):
        super().reverse()
        self.addressmap = (
            ['11', '01', {'path_arc':-PI}],
            ['1/', FadeOut, {'run_time':0.5, 'delay':0}]
        )
        return self


class alg_mul_L(EquationManeuver):
    def __init__(self, **kwargs):
        super().__init__(
            a * b & c,
            b & c / a,
            **kwargs
        )
        self.addressmap = (
            ['00', '11', {'path_arc':PI}],
            #['0*', FadeOut, {'run_time':0.5}],
            [Write, '1/', {'run_time':0.5, 'delay':0.5}]
        )

    def reverse(self):
        super().reverse()
        self.addressmap = (
            ['11', '00', {'path_arc':-PI}],
            ['1/', FadeOut, {'run_time':0.5, 'delay':0}]
        )
        return self


# class alg_pow_R(EquationManeuver):
#     def __init__(self, **kwargs):
#         super().__init__(
#             a**b & c,
#             a & rad(b)(c),
#             **kwargs
#         )








class difference_of_squares_(AlgebraicAction):
    def __init__(self, **kwargs):
        super().__init__(
            a**2 - b**2,
            (a+b)*(a-b),
            **kwargs
        )