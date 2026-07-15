from MF_Tools.dual_compatibility import average_color
# from MF_Tools.dual_compatibility import color_to_rgb, rgb_to_color
# from MF_Tools.dual_compatibility import interpolate_color_by_hsl
# import numpy as np

# manim's built in color averaging function averages them in rgb space with some kinda root mean square
# might be better to implement our own and/or use hsv space but let's try this first
# exists in both GL and CE

# Ok the built in color averaging function sucks in my opinion.
# Tried doing rgb straight average instead of rgb rms but that also sucks


# def average_color(*colors):
#     rgbs = np.array(list(map(color_to_rgb, colors)))
#     return rgb_to_color(rgbs.mean(0))


# Tried ManimGL's interpolate_color_by_hsl but it gave me red+blue=green lol...
# I imagine the polar average is troublesome. I guess we'll be writing our own.

# def average_color(*colors):
# 	if len(colors) == 1:
# 		return colors[0]
# 	elif len(colors) == 2:
# 		return interpolate_color_by_hsl(colors[0], colors[1], 0.5)
# 	else:
# 		raise ValueError('Temporarily sucks')


# What about RGB mean but then shift away from the r=g=b gray line? Need some vector math, could be a good idea.
# Accepting manim's native for now, which is rgb rms on manimgl and rgb straight on manimce.



'#ff0000'
'#800080'
'#0000ff'

'#FC6255'
'#AA93A1'
'#58C4DD'