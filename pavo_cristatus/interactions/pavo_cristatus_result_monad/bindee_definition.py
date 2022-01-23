from typing import Callable


class BindeeDefinition(object):
    def __init__(self, bindee_function, in_parameter_predicate, out_parameter_predicate):
        """
        associates functions to be lifted with predicates
        :param bindee_function: the function that will be lifted
        :param in_parameter_predicate: a predicate to check against the a in (a -> Mb)
        :param out_parameter_predicate: a predicate to check against the b in (a -> Mb)
        """
        self.bindee_function = bindee_function
        self.in_parameter_predicate = in_parameter_predicate
        self.out_parameter_predicate = out_parameter_predicate
