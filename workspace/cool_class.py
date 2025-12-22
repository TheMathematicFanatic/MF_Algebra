from abc import ABC

class CoolBase(ABC):
    def __new__(cls, *args, **kwargs):
        for k,v in kwargs.items():
            if k in cls.__dict__:
                setattr(cls, k, v)
            else:
                raise TypeError(f"{k} is not a valid attribute")
        return super().__new__(cls, *args, **kwargs)


class CoolClass(CoolBase):
    color = 'blue'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


c = CoolClass(color='red')
print(c.color)
c2 = CoolClass(name='bob')
