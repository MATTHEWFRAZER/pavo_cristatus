from typing import Callable, Any


def get_type_check(expected_type):
    """
    Any -> (Any -> bool)
    :param expected_type: type that will be used in the generated boolean check
    :return: a function that will do a boolean check against new types
    """
    return lambda x: type(x) is expected_type
