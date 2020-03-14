import re

__all__ = ["all_whitespace_pattern", "get_function_pattern", "get_class_pattern"]

all_whitespace_pattern =  re.compile(r'\s+')
get_class_pattern = lambda symbol: re.compile(r"^class" + symbol.__name__ + "[(|:]")
get_function_pattern = lambda symbol: re.compile(r"^def" + symbol.__name__ + "\(")