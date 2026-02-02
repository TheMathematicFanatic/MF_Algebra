from ..expressions.numbers.real import pi, tau
from ..expressions.functions.radicals import sqrt
from ..expressions.combiners.operations import Div

unit_circle_dict = {
	# angle  :  (               x,                 y,              y/x  ),
	0        :  (               1,                 0,         Div(0,1)  ),
	pi/6     :  (   Div(sqrt(3),2),         Div(1,2),   Div(1,sqrt(3))  ),
	pi/4     :  (   Div(sqrt(2),2),   Div(sqrt(2),2),                1  ),
	pi/3     :  (         Div(1,2),   Div(sqrt(3),2),          sqrt(3)  ),
	pi/2     :  (                0,                1,         Div(1,0)  ),
	2*pi/3   :  (        -Div(1,2),   Div(sqrt(3),2),         -sqrt(3)  ),
	3*pi/4   :  (  -Div(sqrt(2),2),   Div(sqrt(2),2),               -1  ),
	5*pi/6   :  (  -Div(sqrt(3),2),         Div(1,2),  -Div(1,sqrt(3))  ),
	pi       :  (               -1,                0,                0  ),
	7*pi/6   :  (   Div(sqrt(3),2),        -Div(1,2),   Div(1,sqrt(3))  ),
	5*pi/4   :  (   Div(sqrt(2),2),  -Div(sqrt(2),2),                1  ),
	4*pi/3   :  (         Div(1,2),  -Div(sqrt(3),2),          sqrt(3)  ),
	3*pi/2   :  (                0,               -1,         Div(1,0)  ),
	5*pi/3   :  (        -Div(1,2),  -Div(sqrt(3),2),         -sqrt(3)  ),
	7*pi/4   :  (  -Div(sqrt(2),2),  -Div(sqrt(2),2),               -1  ),
	11*pi/6  :  (  -Div(sqrt(3),2),        -Div(1,2),  -Div(1,sqrt(3))  ),
}


