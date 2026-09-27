api_mode = 'ManimGL'

if api_mode is None:
    from MF_Tools.dual_compatibility import MANIM_TYPE
    api_mode = 'Manim' + MANIM_TYPE

if api_mode == 'ManimGL':
    from .api_manimgl import *

if api_mode is 'ManimCE':
	from .api_manimce import *

if api_mode is 'Web':
	from .api_web import *

if api_mode is 'None':
	from .api_none import *






