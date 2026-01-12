from .expression_core import Expression


class MetaExpression(Expression):
    def __init__(self, name_expression_dict, mode=None):
        self.name_expression_dict = name_expression_dict
        mode = mode or self.name_expression_dict.keys()[0]

    def __getitem__(self, name):
        return self.name_expression_dict[name]
    
    

