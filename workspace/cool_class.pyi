from typing import Callable, TypeVar, dataclass_transform

T = TypeVar('T')

def Factory(make_func: Callable[[], T]) -> T:
	...

@dataclass_transform(kw_only_default=True)
class CoolBase:
	...


