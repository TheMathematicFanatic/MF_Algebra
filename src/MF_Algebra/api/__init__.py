import sys
if sys.implementation.name == 'micropython':
	from .micropython_compatibility import *


from .api_core import decide_api_mode_from_env

api_mode = decide_api_mode_from_env()

if api_mode == 'ManimGL':
	from .api_manimgl import *

if api_mode == 'ManimCE':
	from .api_manimce import *

if api_mode == 'Web':
	from .api_web import *

if api_mode == 'Blender':
	from .api_blender import *

if api_mode == 'None':
	from .api_none import *





