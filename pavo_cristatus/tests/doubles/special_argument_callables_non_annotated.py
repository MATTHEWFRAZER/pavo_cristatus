__all__ = ["all_callables"]

def callable_with_argument_and_keyword_only_argument(a, *, b): pass

def callable_with_all_arguments(a, *args, **kwargs): pass

# not different from callable with all arguments, but needed for testing
def callable_with_all_arguments_and_missing_first_annotation(a, *args, **kwargs): pass

# not different from callable with all arguments, but needed for testing
def callable_with_all_arguments_and_missing_second_annotation(a, *args, **kwargs): pass

# not different from callable with all arguments, but needed for testing
def callable_with_all_arguments_and_missing_third_annotation(a, *args, **kwargs): pass

def callable_with_argument_and_kwargs(a, **kwargs): pass

def callable_with_argument_and_args(a, *args): pass

def callable_with_kwargs(**kwargs): pass

def callable_with_args(*args): pass

def callable_with_keyword_only(*, a): pass

def callable_with_multiple_keyword_only(*, a, b): pass

def callable_with_argument_and_multiple_keyword_only(a, *, b, c): pass

def callable_with_multiple_arguments_and_multiple_keyword_only(a, b, *, c, d): pass

def callable_with_multiple_arguments_and_keyword_only(a, b, *, c): pass

def callable_with_multiple_arguments_and_args(a, b, *args): pass

def callable_with_multiple_arguments_and_kwargs(a, b, **kwargs): pass

all_callables = [
            callable_with_argument_and_keyword_only_argument,
            callable_with_all_arguments,
            callable_with_all_arguments_and_missing_first_annotation,
            callable_with_all_arguments_and_missing_second_annotation,
            callable_with_all_arguments_and_missing_third_annotation,
            callable_with_argument_and_kwargs,
            callable_with_argument_and_args,
            callable_with_kwargs,
            callable_with_args,
            callable_with_keyword_only,
            callable_with_multiple_keyword_only,
            callable_with_argument_and_multiple_keyword_only,
            callable_with_multiple_arguments_and_multiple_keyword_only,
            callable_with_multiple_arguments_and_keyword_only,
            callable_with_multiple_arguments_and_args,
            callable_with_multiple_arguments_and_kwargs
          ]