from .action_core import Action
from .animations import TransformByAddressMap
from MF_Tools import TransformByGlyphMap
from MF_Tools.dual_compatibility import AnimationGroup


class AddressMapAction(Action):
    def __init__(self, *address_map, extra_animations=[], **kwargs):
        super().__init__(**kwargs)
        self.address_map = address_map
        self.extra_animations = extra_animations
    
    def get_animation(self, **kwargs):
        def animation(input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return AnimationGroup(
                TransformByAddressMap(
                    input_exp,
                    output_exp,
                    *self.address_map,
                    **kwargs
                ),
                *self.extra_animations
            )
        return animation


class GlyphMapAction(Action):
    def __init__(self,
        input_exp,
        output_exp,
        *glyph_map,
        extra_animations = [],
        **kwargs
        ):
        action_kwargs = {
            key : kwargs.pop(key)
            for key in Action.__init__.__code__.co_varnames[1:]
            if key in kwargs
        }
        super().__init__(**action_kwargs)
        self.TBGM_kwargs = kwargs
        self.input_exp = input_exp
        self.output_exp = output_exp
        self.glyph_map = glyph_map
        self.extra_animations = extra_animations
    
    def get_animation(self, **kwargs):
        def animation(input_exp, output_exp=None):
            input_exp = self.input_exp
            output_exp = self.output_exp
            return AnimationGroup(
                TransformByGlyphMap(
                    input_exp.mob,
                    output_exp.mob,
                    *self.glyph_map,
                    **self.TBGM_kwargs
                ),
                *self.extra_animations
            )
        return animation

    def get_output_expression(self, input_expression):
        return self.output_exp


class AnimationAction(Action):
    def __init__(self, animation, **kwargs):
        super().__init__(**kwargs)
        self.animation = animation # callable on two mobjects
    
    def get_animation(self, **kwargs):
        def animation(self, input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return self.animation(input_exp.mob, output_exp.mob, **kwargs)
        return animation
