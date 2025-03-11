from manimlib import *


def ir(a,b): #inclusive_range
    return list(range(a,b+1))

class Wait(FadeOut):
    def __init__(self, wait_time, **kwargs):
        self.mobject = VMobject()
        super().__init__(self.mobject, run_time=wait_time, **kwargs)



class TransformByGlyphMap(AnimationGroup):
    def __init__(
        self,
        mobA,
        mobB,
        *glyph_map,
        auto_resolve=False,
        from_copy=False,
        mobA_submobject_index=[],
        mobB_submobject_index=[],
        default_introducer=FadeIn,
        default_remover=FadeOut,
        introduce_individually=False,
        remove_individually=False,
        shift_fades=False,
        auto_resolve_delay=0.5,
        show_indices=False,
        A_index_labels_color=RED_D,
        B_index_labels_color=BLUE_D,
        index_label_height=0.2,
        printing=False,
        **kwargs
        ):

        self.mobA = mobA
        self.mobB = mobB

        A = self.mobA.copy() if from_copy else mobA
        for i in mobA_submobject_index:
            A = A[i]
        B = self.mobB
        for i in mobB_submobject_index:
            B = B[i]
        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []

        def VG(mob, index_list):
            return VGroup(*[mob[i] for i in index_list])
        
        if len(glyph_map)==0: show_indices=True

        for entry in glyph_map:
            if printing:
                print("Glyph map entry: ", entry)
            assert len(entry) in [2, 3], "Invalid glyph_map entry: " + str(entry)
            entry_kwargs = {} if len(entry) == 2 else entry[2]

            if not entry[0] and not entry[1]:
                print("Empty glyph_map entry: " + str(entry))
                show_indices = True
            elif not entry[0] or (isinstance(entry[0], type) and issubclass(entry[0], Animation)):
                Introducer = entry[0] if entry[0] else default_introducer
                introduced_mobs = [B[i] for i in entry[1]] if introduce_individually else [VG(B,entry[1])]
                for mob in introduced_mobs:
                    animations.append(Introducer(
                        mob,
                        **{
                            **kwargs,
                            **({"shift":B.get_center() - A.get_center()} if shift_fades else {}),
                            **{k:v for k,v in entry_kwargs.items() if k != 'delay'}
                        }
                        ))
                    if "delay" in entry_kwargs:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_to_indices += entry[1]
            elif not entry[1] or (isinstance(entry[1], type) and issubclass(entry[1], Animation)):
                Remover = entry[1] if entry[1] else default_remover
                removed_mobs = [A[i] for i in entry[0]] if remove_individually else [VG(A,entry[0])]
                for mob in removed_mobs:
                    animations.append(Remover(
                        mob,
                        **{
                            **kwargs,
                            **({"shift":B.get_center() - A.get_center()} if shift_fades else {}),
                            **{k:v for k,v in entry_kwargs.items() if k != 'delay'}
                        }
                        ))
                    if "delay" in entry_kwargs and entry_kwargs["delay"] != 0:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
            elif len(entry[0]) > 0 and len(entry[1]) > 0:
                animations.append(ReplacementTransform(
                    VGroup(*[A[i].copy() if i in mentioned_from_indices else A[i] for i in entry[0]]),
                    VG(B,entry[1]),
                    **{
                        **kwargs,
                        **{k:v for k,v in entry_kwargs.items() if k != 'delay'}
                        }
                    ))
                if "delay" in entry_kwargs:
                    animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
                mentioned_to_indices += entry[1]
            else:
                raise ValueError("Invalid glyph_map entry: " + str(entry))
        
        
        remaining_from_indices = [i for i in range(len(A)) if i not in mentioned_from_indices]
        remaining_to_indices = [i for i in range(len(B)) if i not in mentioned_to_indices]
        if printing:
            print("All mentioned from indices: ", mentioned_from_indices)
            print("All mentioned to indices: ", mentioned_to_indices)
            print(f"All remaining from indices (length {len(remaining_from_indices)}): ", remaining_from_indices)
            print(f"All remaining to indices (length {len(remaining_to_indices)}):", remaining_to_indices)
        
        if not len(remaining_from_indices) == len(remaining_to_indices) and not auto_resolve:
            print("Error: lengths of unmentioned indices do not match.")
            show_indices = True
        
        if show_indices:
            print("Showing indices...")
            super().__init__(
                ShowCreation(index_labels(A, label_height=index_label_height).set_color(A_index_labels_color).set_z_index(10).set_stroke(color=BLACK, width=3)),
                FadeIn(B.next_to(A, DOWN), shift=DOWN),
                ShowCreation(index_labels(B, label_height=index_label_height).set_color(B_index_labels_color).set_z_index(10).set_stroke(color=BLACK, width=3)),
                Wait(5),
                lag_ratio=0.5
            )
        else:
            if auto_resolve:
                for j in remaining_to_indices:
                    animations.append(Succession(Wait(auto_resolve_delay), default_introducer(B[j])))
                for i in remaining_from_indices:
                    animations.append(Succession(Wait(auto_resolve_delay), default_remover(A[i])))
            else:
                for i,j in zip(remaining_from_indices, remaining_to_indices):
                    animations.append(ReplacementTransform(A[i], B[j], **kwargs))
            super().__init__(*animations, **kwargs)

    def begin(self):
        # Save and later restore mobA so that it is unharmed by the transform
        self.mobA.save_state()
        super().begin()

    def clean_up_from_scene(self, scene):
        # Restore mobA so that it emerges unharmed by the transform
        self.mobA.restore()
        super().clean_up_from_scene(scene)

        # Currently in scene.mobjects are a bunch of orphaned submobjects of mobB.
        # These lines make it so that scene.mobjects actually contains mobB as their parent.
        scene.remove(self.mobB)
        scene.add(self.mobB)







class TransformByAddressMap(TransformByGlyphMap):
    def __init__(self, expA, expB, addressmap, **kwargs):
        glyphmap = self.process_addressmap(mobA, mobB, addressmap)
        super().__init__(expA, expB, *glyphmap, **kwargs)
    
    def process_addressmap(self, mobA, mobB, addressmap):
        pass