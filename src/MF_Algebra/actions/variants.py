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
    def __init__(self, *glyph_map, extra_animations=[], show_indices=False, **kwargs):
        super().__init__(**kwargs)
        self.glyph_map = glyph_map
        self.extra_animations = extra_animations
        self.show_indices = show_indices
    
    def get_animation(self, **kwargs):
        def animation(input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return AnimationGroup(
                TransformByGlyphMap(
                    input_exp.mob,
                    output_exp.mob,
                    *self.glyph_map,
                    show_indices = self.show_indices,
                    **kwargs
                ),
                *self.extra_animations
            )
        return animation


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
