class BindeeDefinition(object):
    def __init__(self, bindee_function, in_parameter_predicate, out_parameter_predicate):
        self.bindee_function = bindee_function
        self.in_parameter_predicate = in_parameter_predicate
        self.out_parameter_predicate = out_parameter_predicate