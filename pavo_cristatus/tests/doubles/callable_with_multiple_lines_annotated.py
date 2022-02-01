from typing import Any

from trochilidae.interoperable_reduce import interoperable_reduce

__all__ = ["all_callables"]

# simple callable start
def callable_with_multiple_lines(a : int,
                                 b : str) -> None: pass

def callable_with_multiple_lines_and_space(a : int,

                                 b : str) -> None: pass

def callable_with_multiple_lines_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> None: pass

def callable_with_multiple_lines_and_ends_with_comma(a : int,
                                                     b : str,) -> None: pass

def callable_with_multiple_lines_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_multiple_spaces(a: int,


                                           b: str) -> None: pass

def callable_with_multiple_lines_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> None: pass
# simple callable end

# simple callable with body start
def callable_with_body_with_multiple_lines(a: int,
                                 b: str) -> bool:
    return True


def callable_with_body_with_multiple_lines_and_space(a: int,

                                           b: str) -> bool:
    return True


def callable_with_body_with_multiple_lines_and_spaces_in_between(a: int,

                                                       b: str

                                                       ) -> bool:
    return True


def callable_with_body_with_multiple_lines_and_ends_with_comma(a: int,
                                                     b: str, ) -> bool:
    return True

def callable_with_body_with_multiple_lines_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> bool:
    return True


def callable_with_body_with_multiple_lines_and_multiple_spaces(a: int,

                                                     b: str) -> bool:
    return True


def callable_with_body_with_multiple_lines_and_annotations_on_separate_lines(a
                                                                   : int,
                                                                   b
                                                                   : str) -> bool:
    return True
# simple callable with body end

# callable that returns a lambda start
def callable_with_multiple_lines_and_lambda(a : int,
                                            b : str) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_and_space(a : int,

                                 b : str) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_and_ends_with_comma(a : int,
                                                     b : str,) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_and_multiple_spaces(a: int,


                                           b: str) -> Any: return lambda : 3

def callable_with_multiple_lines_and_lambda_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> Any: return lambda : 3
# callable that returns a lambda end

# callable that returns a nested lambda start
def callable_with_multiple_lines_and_nested_lambdas(a : int,
                                                    b : str) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambda_and_space(a : int,

                                 b : str) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambda_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambda_and_ends_with_comma(a : int,
                                                     b : str,) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambdas_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambda_and_multiple_spaces(a: int,


                                           b: str) -> Any: return lambda : lambda : 7

def callable_with_multiple_lines_and_nested_lambda_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> Any: return lambda : lambda : 7
# callable that returns a nested lambda end

# callable with logic start
def callable_with_multiple_lines_and_logic(a : int
                                           , b : str) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_and_space(a : int,

                                 b : str) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_and_ends_with_comma(a : int,
                                                     b : str,) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_and_multiple_spaces(a: int,


                                           b: str) -> int: return 3 + 8

def callable_with_multiple_lines_and_logic_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> int: return 3 + 8
# callable with logic end

# callable with logic and no return start
def callable_with_multiple_lines_and_logic_no_return(a : int
                                                     , b : str) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_and_space(a : int,

                                 b : str) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_and_ends_with_comma(a : int,
                                                     b : str,) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_and_multiple_spaces(a: int,


                                           b: str) -> None: 3 + 8

def callable_with_multiple_lines_and_logic_no_return_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> None: 3 + 8
# callable with logic and no return end

# callable that returns a lambda no space start
def callable_with_multiple_lines_and_lambda_and_no_space(a : int,
                                                         b : str) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_space(a : int,

                                 b : str) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_ends_with_comma(a : int,
                                                     b : str,) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_multiple_spaces(a: int,


                                           b: str) -> Any: return lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> Any: return lambda:3
# callable that returns a lambda no space end

# callable that returns a lambda no space no return start
def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return(a : int,
                                                         b : str) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_space(a : int,

                                 b : str) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_spaces_in_between(a : int,

                                 b : str

                                                       ) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_ends_with_comma(a : int,
                                                     b : str,) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_with_comma_on_separate_line(a : int,
                                                                        b : str
                                                                       ,) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_multiple_spaces(a: int,


                                           b: str) -> None: lambda:3

def callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_annotations_on_separate_lines(a
                                                     : int,
                                                     b
                                                     : str) -> None: lambda:3
# callable that returns a lambda no space no return end

# callable with multiple lines with one argument start
def callable_with_multiple_lines_with_one_argument(a : int
                                                   ) -> Any: pass

def callable_with_multiple_lines_with_one_argument_and_space(a : int

                                 ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_space_and_spaces_in_between(a : int

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_ends_with_comma_on_separate_line(a : int
                                                                       ,) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_ends_with_comma(a : int,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_multiple_spaces(a: int


                                           ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotations_on_separate_lines(a
                                                     : int) -> None: pass
# callable with multiple lines with one argument end

# callable with multiple lines with one argument and annotation on separate line start
def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line(a
                                                                                   : int) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_space(a
                                                                                             : int

                                 ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_space_and_spaces_in_between(a
                                                                                                                   : int

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_ends_with_comma_on_separate_line(a
                                                                                                                        : int
                                                                       ,) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_ends_with_comma(a
                                                                                                       : int,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_multiple_spaces(a
                                                                                                       : int


                                           ) -> None: pass

# callable with multiple lines with one argument and annotation on separate line end

# call with multiple lines with no argument start
def callable_with_multiple_lines_with_no_argument(
) -> None: pass

def callable_with_multiple_lines_with_no_argument_and_space(

                                 ) -> None: pass

def callable_with_multiple_lines_with_no_argument_and_multiple_spaces(


                                           ) -> None: pass
# call with multiple lines with no argument end

# callable with multiple lines and varargs only start
def callable_with_multiple_lines_and_varargs_only(*args : Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_varargs_only_and_space(*args : Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_spaces_in_between_with_comma(*args : Any

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_spaces_in_between(*args

                                                                              : Any

                                                       ) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_ends_with_comma_on_separate_line(*args : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_ends_with_comma(*args : Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_multiple_spaces(*args : Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_varargs_only_and_annotations_on_separate_lines(*args
                                                     : int) -> None: pass
# callable with multiple lines and varargs only end

# callable with multiple lines and kwargs only start
def callable_with_multiple_lines_and_kwargs_only(**kwargs: Any
                                                 ) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_space(**kwargs: Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_spaces_in_between_with_comma(**kwargs: Any

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_spaces_in_between(**kwargs

                                                                       : Any

                                                                     ) -> Any: pass

def callable_with_multiple_lines_and_kwargs_only_and_ends_with_comma_on_separate_line(**kwargs: Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_ends_with_comma(**kwargs: Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_multiple_spaces(**kwargs: Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_kwargs_only_and_annotations_on_separate_lines(**kwargs
                                                     : Any) -> None: pass
# callable with multiple lines and kwargs only end

# callable with multiple lines and keyword only start
def callable_with_multiple_lines_and_keyword_only(*, a : Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_and_space(*, a : Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_and_spaces_in_between_with_comma(*, a : Any

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_and_spaces_in_between(*, a

                                                                       : Any

                                                                     ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_and_ends_with_comma_on_separate_line(*, a : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_keyword_only_and_ends_with_comma(*, a : Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_and_multiple_spaces(*, a : Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_and_annotations_on_separate_lines(*, a
                                                     : Any) -> None: pass

def callable_with_multiple_lines_and_keyword_only_annotation_on_separate_line(*, a
: Any
                                                 ) -> Any: pass
# callable with multiple lines and keyword only end

# callable with multiple lines and keyword only with star on top start
def callable_with_multiple_lines_and_keyword_only_with_star_on_top(*
                                                                        , a : Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_space(*
                                                                             , a : Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between_with_comma(*
                                                                                                    , a : Any

                                                                                   ,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between_annotation(*
                                                                                         , a

                                                                       : Any

                                                                     ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_ends_with_comma_on_separate_line(*
                                                                                                        , a : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_ends_with_comma(*, a : Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_multiple_spaces(*, a : Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_annotations_on_separate_lines(*, a
                                                     : Any) -> None: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_annotation_on_separate_line(*, a
: Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_annotation_on_separate_line_keyword_on_separate_line(*
                                                                        , a
                                                                                                    : Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_start_on_top_and_space(*
                                                                                  , a : Any

                                                           ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between(*

                                                                                  , a : Any

                                                           ) -> Any: pass

def callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_multiple_spaces_with_annotation_on_separate_line(*
                                                                                            , a : Any


                                                                     ) -> Any: pass
# callable with multiple lines and keyword only with star on top end

# callable with multiple lines and multiple keyword only start
def callable_with_multiple_lines_and_multiple_keyword_only(*, a : Any, b : Any
                                                 ) -> Any: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_space(*, a : Any, b : Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_spaces_in_between_with_comma(*, a : Any

                                                                                   ,b : Any

,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_spaces_in_between(*, a

                                                                       : Any,

                                                                                 b

                                                                                 :Any,

                                                                     ) -> Any: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_ends_with_comma_on_separate_line(*, a : Any, b : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_ends_with_comma(*, a : Any, b: Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_multiple_spaces(*, a : Any, b : Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_multiple_keyword_only_and_annotations_on_separate_lines(*, a
                                                     : Any,
                                                                                             b
                                                                                             :Any) -> None: pass
# callable with multiple lines and multiple keyword only end

# callable with argument and keyword only argument start
def callable_with_multiple_lines_and_argument_and_keyword_only_argument(a : int,
                                                     *,
                                                     b : int) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_space(a : int, *, b : Any

                                 ) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_spaces_in_between_with_comma(a : int, *

                                                                                   ,b : Any

                                                                                                         ,

                                                       ) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_spaces_in_between(a

                                                                                              : int,

                                                                                              *,

                                                                                 b

                                                                                 :Any,

                                                                     ) -> Any: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_ends_with_comma_on_separate_line(a : int, *, b : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_ends_with_comma(a : int, *, b: Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_multiple_spaces(a : int, *, b : Any


                                           ) -> None: pass

def callable_with_multiple_lines_and_argument_and_keyword_only_argument_with_space_between_arguments(a : int, *,

                                                                                             b
                                                                                             :Any) -> None: pass
# callable with argument and keyword only argument end

# callable with all arguments start
def callable_with_multiple_lines_with_all_arguments(a : int,
                                                    *args : Any,
                                                    **kwargs : Any) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_space(a : int, *args : Any, **kwargs : Any

                                 ) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_spaces_in_between_with_comma(a : int,

                                                                                   *args : Any,

                                                                                     **kwargs : Any

                                                                                     ,

                                                       ) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_spaces_in_between(a

                                                                          : int,

                                                                          *args

                                                                          : Any,

                                                                          **kwargs

                                                                          : Any

                                                                     ) -> Any: pass


def callable_with_multiple_lines_with_all_arguments_and_no_spaces_in_between(a
                                                                          : int,
                                                                          *args
                                                                          : Any,
                                                                          **kwargs
                                                                          : Any
                                                                          ) -> Any: pass

def callable_with_multiple_lines_with_all_arguments_and_ends_with_comma_on_separate_line(a : int, *args : Any, **kwargs : Any
                                                                       ,) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_ends_with_comma(a : int, *args : Any, **kwargs : Any,
                                                                                        ) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_multiple_spaces(a : int, *args : Any, **kwargs : Any


                                           ) -> None: pass

def callable_with_multiple_lines_with_all_arguments_and_annotations_on_separate_lines(a
                                                                                      : int,

                                                                                             *args
                                                                                             :Any,

                                                                                      **kwargs
                                                                                      : Any) -> None: pass
# callable with all arguments end

# callable with argument and kwargs start
def callable_with_multiple_lines_and_argument_and_kwargs(a : int,
                                                         **kwargs : Any) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_space(a : int,
                                                         **kwargs : Any

                                                                   ) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_spaces_in_between_with_comma(a : int,

                                                         **kwargs : Any

,

                                                                                     ) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_spaces_in_between(a

                                                                               : int,

                                                         **kwargs

                                                         : Any

                                                                          ) -> Any: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_no_spaces_in_between(a
                                                                             : int,
                                                                             **kwargs
                                                                             : Any
                                                                             ) -> Any: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_ends_with_comma_on_separate_line(a: int, **kwargs: Any
                                                                                         , ) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_ends_with_comma(a: int, **kwargs: Any,
                                                                        ) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_multiple_spaces(a: int, **kwargs: Any


                                                                        ) -> None: pass


def callable_with_multiple_lines_and_argument_and_kwargs_and_annotations_on_separate_lines(a
                                                                                      : int,

                                                                                      **kwargs
                                                                                      : Any) -> None: pass
# callable with argument and kwargs end

# callable with argument and args start
def callable_with_multiple_lines_with_argument_and_args(a : int,
                                    *args : Any) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_space(a: int,
                                                                   *args: Any

                                                                   ) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_spaces_in_between_with_comma(a: int,

                                                                                          *args: Any

                                                                                          ,

                                                                                          ) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_spaces_in_between(a

                                                                               : int,

                                                                               *args

                                                                               : Any

                                                                               ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_args_and_no_spaces_in_between(a
                                                                                  : int,
                                                                                  *args
                                                                                  : Any
                                                                                  ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_args_and_ends_with_comma_on_separate_line(a: int, *args: Any
                                                                                              , ) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_ends_with_comma(a: int, *args: Any,
                                                                             ) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_multiple_spaces(a: int, *args: Any


                                                                             ) -> None: pass


def callable_with_multiple_lines_with_argument_and_args_and_annotations_on_separate_lines(a
                                                                                           : int,

                                                                                           *args
                                                                                           : Any) -> None: pass
# callable with argument and args end

# callable with argument and keyword only start
def callable_with_multiple_lines_with_argument_and_keyword_only(a : int,
                                                                *,
                                                                b : int) -> None: pass

def callable_with_multiple_lines_with_argument_and_keyword_only_and_space(a: int,
                                                                   *,
                                                                    b: int

                                                                   ) -> None: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_spaces_in_between_with_comma(a: int,

                                                                                          *,

                                                                                                 b : int

                                                                                          ,

                                                                                          ) -> None: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_spaces_in_between(a

                                                                               : int,

                                                                               *,

                                                                                      b

                                                                               : int

                                                                               ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_no_spaces_in_between(a
                                                                                  : int,
                                                                                  *,
                                                                                b
                                                                                  : int
                                                                                  ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_ends_with_comma_on_separate_line(a: int, *, b : int
                                                                                              , ) -> None: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_ends_with_comma(a: int, *, b : int,
                                                                             ) -> None: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_multiple_spaces(a: int, *, b : int


                                                                             ) -> None: pass


def callable_with_multiple_lines_with_argument_and_keyword_only_and_annotations_on_separate_lines(a
                                                                                           : int,

                                                                                           *,

                                                                                          b : int) -> None: pass
# callable with argument and keyword only end

# callable with argument and multiple keyword only start
def callable_with_multiple_lines_with_argument_and_multiple_keyword_only(a : int,
                                                                         *,
                                                                         b : int,
                                                                         c : int) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_space(a: int,
                                                                          *,
                                                                          b: int,
                                                                        c :int

                                                                          ) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_spaces_in_between_with_comma(a: int,

                                                                                                 *,

                                                                                                 b: int,

                                                                                                c : int

                                                                                                 ,

                                                                                                 ) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_spaces_in_between(a

                                                                                      : int,

                                                                                      *,

                                                                                      b

                                                                                      : int,

                                                                                    c

                                                                                    : int

                                                                                      ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_no_spaces_in_between(a
                                                                                         : int,
                                                                                         *,
                                                                                         b
                                                                                         : int,
                                                                                        c
                                                                                        : int
                                                                                         ) -> Any: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_ends_with_comma_on_separate_line(a: int, *, b: int, c : int
                                                                                                     , ) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_ends_with_comma(a: int, *, b: int, c : int,
                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_multiple_spaces(a: int, *, b: int, c : int


                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_annotations_on_separate_lines(a
                                                                                                  : int,

                                                                                                  *,

                                                                                                  b: int,

                                                                                                c : int) -> None: pass
# callable with argument and multiple keyword only end

# callable with multiple arguments and multiple keyword only start
def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only(a : int,
                                                                                   b : int,
                                                                                   *,
                                                                                   c : int,
                                                                                   d : int) -> None: pass

def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_space(a: int,
                                                                          b : int,
                                                                          *,
                                                                        c :int,
                                                                        d : int

                                                                          ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_spaces_in_between_with_comma(a: int,

                                                                                                                    b : int,

                                                                                                 *,

                                                                                                c : int,

                                                                                                d : int

                                                                                                 ,

                                                                                                 ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_spaces_in_between(a

                                                                                      : int,

                                                                                        b

                                                                                    :int,

                                                                                      *,

                                                                                      c

                                                                                      : int,

                                                                                    d

                                                                                    : int

                                                                                      ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_no_spaces_in_between(a
                                                                                         : int,
                                                                                                            b
:int,
                                                                                         *,
                                                                                         c
                                                                                         : int,
                                                                                        d
                                                                                        : int
                                                                                         ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_ends_with_comma_on_separate_line(a: int, b : int, *, c: int, d : int
                                                                                                     , ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_ends_with_comma(a: int, b : int, *, c: int, d : int,
                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_multiple_spaces(a: int, b : int, *, c: int, d : int


                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_annotations_on_separate_lines(a
                                                                                                  : int,

                                                                                                 b : int,

                                                                                                  *,

                                                                                                  c: int,

                                                                                                d : int) -> None: pass

# callable with multiple arguments and multiple keyword only end

# callable with multiple arguments and keyword only start
def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only(a : int,
                                                                                   b : int,
                                                                                   *,
                                                                                   c : int) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_space(a: int,
                                                                                             b: int,
                                                                                             *,
                                                                                             c: int

                                                                                             ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_spaces_in_between_with_comma(
        a: int,

        b: int,

        *,

        c: int

        ,

        ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_spaces_in_between(a

                                                                                                         : int,

                                                                                                         b

                                                                                                         : int,

                                                                                                         *,

                                                                                                         c

                                                                                                         : int

                                                                                                         ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_no_spaces_in_between(a
                                                                                                            : int,
                                                                                                            b
                                                                                                            : int,
                                                                                                            *,
                                                                                                            c
                                                                                                            : int
                                                                                                            ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_ends_with_comma_on_separate_line(
        a: int, b: int, *, c: int
        , ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_ends_with_comma(a: int, b: int, *, c: int,
                                                                                                       ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_multiple_spaces(a: int, b: int, *, c: int


                                                                                                       ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_annotations_on_separate_lines(a
                                                                                                                     : int,

                                                                                                                     b: int,

                                                                                                                     *,

                                                                                                                     c: int) -> None: pass
# callable with multiple arguments and keyword only end

# callable with multiple arguments and kwargs start
def callable_with_multiple_lines_with_multiple_arguments_and_kwargs(a : int,
                                                                    b : int,
                                                                    **kwargs : Any) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_space(a: int,
                                                                            b : int,
                                                                              **kwargs : Any

                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_spaces_in_between_with_comma(
        a: int,

        b: int,

        **kwargs : Any

        ,

) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_spaces_in_between(a

                                                                                                : int,

                                                                                                b

                                                                                                : int,

                                                                                                **kwargs : Any,

                                                                                                ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_no_spaces_in_between(a
                                                                                                   : int,
                                                                                                   b
                                                                                                   : int,
                                                                                                   **kwargs
                                                                                                    : Any
                                                                                                   ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_ends_with_comma_on_separate_line(a: int, b: int, **kwargs : Any
        , ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_ends_with_comma(a: int, b: int, **kwargs : Any,
                                                                                              ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_multiple_spaces(a: int, b: int, **kwargs : Any


                                                                                              ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_annotations_on_separate_lines(a
                                                                                                            : int,

                                                                                                            b: int,

                                                                                                            **kwargs : Any) -> None: pass
# callable with multiple arguments and kwargs end

# callable with multiple arguments and args start
def callable_with_multiple_lines_with_multiple_arguments_and_args(a : int,
                                                                    b : int,
                                                                    *args : Any) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_space(a: int,
                                                                            b : int,
                                                                              *args : Any

                                                                                    ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_spaces_in_between_with_comma(
        a: int,

        b: int,

        *args : Any

        ,

) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_spaces_in_between(a

                                                                                                : int,

                                                                                                b

                                                                                                : int,

                                                                                                *args : Any,

                                                                                                ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_no_spaces_in_between(a
                                                                                                   : int,
                                                                                                   b
                                                                                                   : int,
                                                                                                   *args
                                                                                                   : Any
                                                                                                   ) -> Any: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_ends_with_comma_on_separate_line(a: int, b: int, *args : Any
        , ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_ends_with_comma(a: int, b: int, *args : Any,
                                                                                              ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_multiple_spaces(a: int, b: int, *args : Any


                                                                                              ) -> None: pass


def callable_with_multiple_lines_with_multiple_arguments_and_args_and_annotations_on_separate_lines(a
                                                                                                            : int,

                                                                                                            b: int,

                                                                                                            *args : Any) -> None: pass
# callable with multiple arguments and args end

class CallableTestConfiguration(object):
    def __init__(self, callables, expected_callable_postfix):
        self.callables = callables
        self.expected_callable_postfix = expected_callable_postfix

all_callables = [
# simple callable start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines,
            callable_with_multiple_lines_and_space,
            callable_with_multiple_lines_and_spaces_in_between,
            callable_with_multiple_lines_and_ends_with_comma,
            callable_with_multiple_lines_with_comma_on_separate_line,
            callable_with_multiple_lines_and_multiple_spaces,
            callable_with_multiple_lines_and_annotations_on_separate_lines
        ],
        "(a, b): pass"
    ),
# simple callable end

# simple callable with body start
    CallableTestConfiguration
    (
        [
            callable_with_body_with_multiple_lines,
            callable_with_body_with_multiple_lines_and_ends_with_comma
        ],
        "(a, b):\n\n    return True"
    ),

    CallableTestConfiguration
    (
        [
            callable_with_body_with_multiple_lines_and_space,
            callable_with_body_with_multiple_lines_with_comma_on_separate_line,
            callable_with_body_with_multiple_lines_and_multiple_spaces
        ],
        "(a, b):\n\n\n    return True"
    ),

    CallableTestConfiguration
    (
        [
            callable_with_body_with_multiple_lines_and_spaces_in_between
        ],
        "(a, b):\n\n\n\n\n    return True"
    ),

    CallableTestConfiguration
    (
        [
            callable_with_body_with_multiple_lines_and_annotations_on_separate_lines
        ],
        "(a, b):\n\n\n\n    return True"
    ),
# simple callable with body end

# callable that returns a lambda start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_lambda,
            callable_with_multiple_lines_and_lambda_and_space,
            callable_with_multiple_lines_and_lambda_and_spaces_in_between,
            callable_with_multiple_lines_and_lambda_and_ends_with_comma,
            callable_with_multiple_lines_and_lambda_with_comma_on_separate_line,
            callable_with_multiple_lines_and_lambda_and_multiple_spaces,
            callable_with_multiple_lines_and_lambda_and_annotations_on_separate_lines
        ],
        "(a, b): return lambda : 3"
    ),
# callable that returns a lambda end

# callable that returns a nested lambda start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_nested_lambdas,
            callable_with_multiple_lines_and_nested_lambda_and_space,
            callable_with_multiple_lines_and_nested_lambda_and_spaces_in_between,
            callable_with_multiple_lines_and_nested_lambda_and_ends_with_comma,
            callable_with_multiple_lines_and_nested_lambdas_with_comma_on_separate_line,
            callable_with_multiple_lines_and_nested_lambda_and_multiple_spaces,
            callable_with_multiple_lines_and_nested_lambda_and_annotations_on_separate_lines
        ],
        "(a, b): return lambda : lambda : 7"
    ),
# callable that returns a nested lambda end

# callable with logic start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_logic,
            callable_with_multiple_lines_and_logic_and_space,
            callable_with_multiple_lines_and_logic_and_spaces_in_between,
            callable_with_multiple_lines_and_logic_and_ends_with_comma,
            callable_with_multiple_lines_and_logic_with_comma_on_separate_line,
            callable_with_multiple_lines_and_logic_and_multiple_spaces,
            callable_with_multiple_lines_and_logic_and_annotations_on_separate_lines
        ],
        "(a, b): return 3 + 8"
    ),
# callable with logic end

# callable with logic and no return start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_logic_no_return,
            callable_with_multiple_lines_and_logic_no_return_and_space,
            callable_with_multiple_lines_and_logic_no_return_and_spaces_in_between,
            callable_with_multiple_lines_and_logic_no_return_and_ends_with_comma,
            callable_with_multiple_lines_and_logic_no_return_with_comma_on_separate_line,
            callable_with_multiple_lines_and_logic_no_return_and_multiple_spaces,
            callable_with_multiple_lines_and_logic_no_return_and_annotations_on_separate_lines
        ],
        "(a, b): 3 + 8"
    ),
# callable with logic and no return end

# callable that returns a lambda no space start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_lambda_and_no_space,
            callable_with_multiple_lines_and_lambda_and_no_space_and_space,
            callable_with_multiple_lines_and_lambda_and_no_space_and_spaces_in_between,
            callable_with_multiple_lines_and_lambda_and_no_space_and_ends_with_comma,
            callable_with_multiple_lines_and_lambda_and_no_space_with_comma_on_separate_line,
            callable_with_multiple_lines_and_lambda_and_no_space_and_multiple_spaces,
            callable_with_multiple_lines_and_lambda_and_no_space_and_annotations_on_separate_lines
        ],
        "(a, b): return lambda :3"
    ),
# callable that returns a lambda no space end

# callable that returns a lambda no space no return start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_space,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_spaces_in_between,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_ends_with_comma,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_with_comma_on_separate_line,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_multiple_spaces,
            callable_with_multiple_lines_and_lambda_and_no_space_and_no_return_and_annotations_on_separate_lines
        ],
        "(a, b): lambda :3"
    ),
# callable that returns a lambda no space no return end

# callable with multiple lines with one argument start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_one_argument,
            callable_with_multiple_lines_with_one_argument_and_space,
            callable_with_multiple_lines_with_one_argument_and_space_and_spaces_in_between,
            callable_with_multiple_lines_with_one_argument_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_one_argument_and_ends_with_comma,
            callable_with_multiple_lines_with_one_argument_and_multiple_spaces
        ],
        "(a): pass"
    ),
# callable with multiple lines with one argument end

# callable with multiple lines with one argument and annotation on separate line start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_one_argument_and_annotations_on_separate_lines,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_space,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_space_and_spaces_in_between,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_ends_with_comma,
            callable_with_multiple_lines_with_one_argument_and_annotation_on_separate_line_and_multiple_spaces
        ],
        "(a): pass"
    ),
# callable with multiple lines with one argument and annotation on separate line end

# call with multiple lines with no argument start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_no_argument,
            callable_with_multiple_lines_with_no_argument_and_space,
            callable_with_multiple_lines_with_no_argument_and_multiple_spaces
        ],
        "(): pass"
    ),
# call with multiple lines with no argument end

# callable with multiple lines and varargs only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_varargs_only,
            callable_with_multiple_lines_and_varargs_only_and_space,
            callable_with_multiple_lines_and_varargs_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_varargs_only_and_spaces_in_between,
            callable_with_multiple_lines_and_varargs_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_varargs_only_and_ends_with_comma,
            callable_with_multiple_lines_and_varargs_only_and_multiple_spaces,
            callable_with_multiple_lines_and_varargs_only_and_annotations_on_separate_lines
        ],
        "(*args): pass"
    ),
# callable with multiple lines and varargs only end

# callable with multiple lines and kwargs only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_kwargs_only,
            callable_with_multiple_lines_and_kwargs_only_and_space,
            callable_with_multiple_lines_and_kwargs_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_kwargs_only_and_spaces_in_between,
            callable_with_multiple_lines_and_kwargs_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_kwargs_only_and_ends_with_comma,
            callable_with_multiple_lines_and_kwargs_only_and_multiple_spaces,
            callable_with_multiple_lines_and_kwargs_only_and_annotations_on_separate_lines
        ],
        "(**kwargs): pass"
    ),
# callable with multiple lines and kwargs only end

# callable with multiple lines and keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_keyword_only,
            callable_with_multiple_lines_and_keyword_only_and_space,
            callable_with_multiple_lines_and_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_and_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_and_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_and_keyword_only_and_annotations_on_separate_lines,
            callable_with_multiple_lines_and_keyword_only_annotation_on_separate_line
        ],
        "(*, a): pass"
    ),
# callable with multiple lines and keyword only end

# callable with multiple lines and keyword only with star on top start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_keyword_only_with_star_on_top,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_space,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between_annotation,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_ends_with_comma,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_multiple_spaces,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_annotations_on_separate_lines,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_annotation_on_separate_line,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_annotation_on_separate_line_keyword_on_separate_line,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_space,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_spaces_in_between,
            callable_with_multiple_lines_and_keyword_only_with_star_on_top_and_multiple_spaces_with_annotation_on_separate_line
        ],
        "(*, a): pass"
    ),
# callable with multiple lines and keyword only with star on top end

# callable with multiple lines and multiple keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_multiple_keyword_only,
            callable_with_multiple_lines_and_multiple_keyword_only_and_space,
            callable_with_multiple_lines_and_multiple_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_multiple_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_and_multiple_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_multiple_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_and_multiple_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_and_multiple_keyword_only_and_annotations_on_separate_lines
        ],
        "(*, a, b): pass"
    ),
# callable with multiple lines and multiple keyword only end

# callable with argument and keyword only argument start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_argument_and_keyword_only_argument,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_space,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_spaces_in_between,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_ends_with_comma,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_and_multiple_spaces,
            callable_with_multiple_lines_and_argument_and_keyword_only_argument_with_space_between_arguments
        ],
        "(a, *, b): pass"
    ),
# callable with argument and keyword only argument end

# callable with all arguments start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_all_arguments,
            callable_with_multiple_lines_with_all_arguments_and_space,
            callable_with_multiple_lines_with_all_arguments_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_all_arguments_and_spaces_in_between,
            callable_with_multiple_lines_with_all_arguments_and_no_spaces_in_between,
            callable_with_multiple_lines_with_all_arguments_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_all_arguments_and_ends_with_comma,
            callable_with_multiple_lines_with_all_arguments_and_multiple_spaces,
            callable_with_multiple_lines_with_all_arguments_and_annotations_on_separate_lines
        ],
        "(a, *args, **kwargs): pass"
    ),
# callable with all arguments end

# callable with argument and kwargs start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_and_argument_and_kwargs,
            callable_with_multiple_lines_and_argument_and_kwargs_and_space,
            callable_with_multiple_lines_and_argument_and_kwargs_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_and_argument_and_kwargs_and_spaces_in_between,
            callable_with_multiple_lines_and_argument_and_kwargs_and_no_spaces_in_between,
            callable_with_multiple_lines_and_argument_and_kwargs_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_and_argument_and_kwargs_and_ends_with_comma,
            callable_with_multiple_lines_and_argument_and_kwargs_and_multiple_spaces,
            callable_with_multiple_lines_and_argument_and_kwargs_and_annotations_on_separate_lines
        ],
        "(a, **kwargs): pass"
    ),
# callable with argument and kwargs end

# callable with argument and args start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_argument_and_args,
            callable_with_multiple_lines_with_argument_and_args_and_space,
            callable_with_multiple_lines_with_argument_and_args_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_argument_and_args_and_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_args_and_no_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_args_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_argument_and_args_and_ends_with_comma,
            callable_with_multiple_lines_with_argument_and_args_and_multiple_spaces,
            callable_with_multiple_lines_with_argument_and_args_and_annotations_on_separate_lines
        ],
        "(a, *args): pass"
    ),
# callable with argument and args end

# callable with argument and keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_argument_and_keyword_only,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_space,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_no_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_with_argument_and_keyword_only_and_annotations_on_separate_lines
        ],
        "(a, *, b): pass"
    ),
# callable with argument and key word only end

# callable with argument and multiple keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_space,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_no_spaces_in_between,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_with_argument_and_multiple_keyword_only_and_annotations_on_separate_lines
        ],
        "(a, *, b, c): pass"
    ),
# callable with argument and multiple key word only end

# callable with multiple arguments and multiple keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_space,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_no_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_with_multiple_arguments_and_multiple_keyword_only_and_annotations_on_separate_lines
        ],
        "(a, b, *, c, d): pass"
    ),
# callable with multiple arguments and multiple key word only end

# callable with multiple arguments and keyword only start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_space,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_no_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_ends_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_multiple_spaces,
            callable_with_multiple_lines_with_multiple_arguments_and_keyword_only_and_annotations_on_separate_lines
        ],
        "(a, b, *, c): pass"
    ),
# callable with multiple arguments and key word only end

# callable with multiple arguments and kwargs start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_space,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_no_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_ends_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_multiple_spaces,
            callable_with_multiple_lines_with_multiple_arguments_and_kwargs_and_annotations_on_separate_lines
        ],
        "(a, b, **kwargs): pass"
    ),
# callable with multiple arguments and kwargs end

# callable with multiple arguments and args start
    CallableTestConfiguration
    (
        [
            callable_with_multiple_lines_with_multiple_arguments_and_args,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_space,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_spaces_in_between_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_no_spaces_in_between,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_ends_with_comma_on_separate_line,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_ends_with_comma,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_multiple_spaces,
            callable_with_multiple_lines_with_multiple_arguments_and_args_and_annotations_on_separate_lines
        ],
        "(a, b, *args): pass"
    ),
# callable with multiple arguments and args end
]

def flatten_callables(x, y):
    x.extend([(c, y.expected_callable_postfix) for c in y.callables])
    return x

all_callables = interoperable_reduce(flatten_callables, all_callables, [])