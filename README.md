## Introduction

This is a Manim plugin (**still under construction**) for algebra animations that are beautiful, meaningful, and automatic. It is compatible with both ManimGL and Manim Community Edition. It consists of a few key components: 
- Expression: These objects contain a tree structure representing algebra expressions/equations, such as `3x^2`, `5+9`, and `sin(y)=14e^x`, as well as a method for producing a corresponding Tex/MathTex mobject.
- Action: These objects contain methods to convert between expressions/equations, such as adding something to both sides, or substituting a variable for a value. This conversion can be static or animated.
- Timeline: These objects contain an alternating sequence of expressions and actions, and methods for automatically determining these sequences, and managing mobject adding/removing and action animations. For example, the Solve timeline takes an equation and tries to solve it for a certain variable, filling itself in with actions and expressions to achieve that goal.


Documentation and tutorials coming in the future. \
Please consider supporting this project! \
For now, check in workspace for examples!


## Installation

This package can be installed with
```
pip install MF_Algebra
```
and is imported with the same name. I recommend
```py
from manimlib import *
from MF_Algebra import *
```
or
```py
from manim import *
from MF_Algebra import *
```


## License Summary

This project is **free for individuals and educators** who create publicly available educational content.  
✅ Examples: YouTube videos, TikToks, livestreams, tutorials, classroom materials (even if ad-monetized but free to watch).  

🚫 **Commercial use requires a paid license.**  
Examples: websites or apps where users interact with the software (e.g. “solve any equation” sites), paid courses, subscription platforms, paywalled content, textbooks, or e-books.  

🙏 If you’re a free user, please consider supporting development via [GitHub Sponsors](https://github.com/sponsors/YOUR_USERNAME) or [Buy Me A Coffee](buymeacoffee.com/themathematicfanatic).  
💼 For commercial licensing inquiries, contact: [johnconnelltutor@gmail.com].

See [LICENSE](./LICENSE.md) for the full terms.









