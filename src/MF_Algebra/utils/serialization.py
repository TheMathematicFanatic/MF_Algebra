import os
from .base_class import MF_Base


def save_to_file(obj:MF_Base, filename:str) -> None:
	import dill as pickle
	os.makedirs('saved_objects', exist_ok=True)
	path = os.path.join('saved_objects', filename)
	with open(path, 'wb') as f:
		pickle.dump(obj, f)

def load_from_file(filename:str) -> MF_Base:
	import dill as pickle
	path = os.path.join('saved_objects', filename)
	with open(path, 'rb') as f:
		return pickle.load(f)

