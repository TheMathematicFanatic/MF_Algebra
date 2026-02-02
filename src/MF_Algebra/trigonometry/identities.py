from ..algebra import AlgebraicAction
from .trigonometry_core import *
from ..expressions import a,b,t,e,i


class TrigIdentity(AlgebraicAction):
    pass


class def_tan(TrigIdentity):
    template1 = tan(t)
    template2 = sin(t)/cos(t)
    addressmap = [['0f','00f'], ['0f','10f'], [[],'/']]

class def_cot(TrigIdentity):
    template1 = tan(t)
    template2 = cos(t)/sin(t)
    addressmap = [['0f','00f'], ['0f','10f'], [[],'/']]

class def_sec(TrigIdentity):
    template1 = sec(t)
    template2 = 1/cos(t)
    addressmap = [['0f','10f'], [[],'/0']]

class def_csc(TrigIdentity):
    template1 = csc(t)
    template2 = 1/sin(t)
    addressmap = [['0f','10f'], [[],'/0']]



class pythagorean(TrigIdentity):
    template1 = (sin**2)(t) + (cos**2)(t)
    template2 = 1
    addressmap = [['','']]

class pythagorean_tan(TrigIdentity):
    template1 = (tan**2)(t) + 1
    template2 = (sec**2)(t)
    addressmap = [['','']]

class pythagorean_cot(TrigIdentity):
    template1 = 1 + (cot**2)(t)
    template2 = (csc**2)(t)
    addressmap = [['','']]

class double_angle_sin(TrigIdentity):
    template1 = sin(2*t)
    template2 = 2*sin(t)*cos(t)

class double_angle_cos(TrigIdentity):
    template1 = cos(2*t)
    template2 = (cos**2)(t) - (sin**2)(t)

class double_angle_tan(TrigIdentity):
    template1 = tan(2*t)
    template2 = (2*tan(t)) / (1 + (tan**2)(t))

class sin_add(TrigIdentity):
    template1 = sin(a+b)
    template2 = sin(a)*cos(b) + cos(a)*sin(b)
    addressmap = [['1+','+']]

class sin_sub(TrigIdentity):
    template1 = sin(a-b)
    template2 = sin(a)*cos(b) - cos(a)*sin(b)
    addressmap = [['1-','-']]

class cos_add(TrigIdentity):
    template1 = cos(a+b)
    template2 = cos(a)*cos(b) - sin(a)*sin(b)
    addressmap = [['1+','-']]

class cos_sub(TrigIdentity):
    template1 = cos(a-b)
    template2 = cos(a)*cos(b) + sin(a)*sin(b)
    addressmap = [['1-','+']]

