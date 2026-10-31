from .cool_class import *

class CoolSubclass(CoolBase):
	color: str = 'blue'
	numbers: list[int] = Factory(lambda: [1,2,3])
	# def __init__(self, **kwargs):
	# 	super().__init__(**kwargs)
	# 	print(f'object initialized with color={self.color}')



c = CoolSubclass(

)

import json

json.JSONEncoder()