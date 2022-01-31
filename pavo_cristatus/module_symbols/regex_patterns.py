import re

__all__ = ["get_function_pattern", "get_class_pattern"]

# some patterns that we use throughout the project

get_class_pattern = lambda symbol_name: re.compile(r"class\s+" + symbol_name + "\s*[(|:]")
get_function_pattern = lambda symbol_name: re.compile(r"def\s+" + symbol_name + "\s*\(")
