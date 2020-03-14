def get_type_check(expected_type):
    return lambda x: type(x) is expected_type
