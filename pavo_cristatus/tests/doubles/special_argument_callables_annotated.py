from typing import Any

__all__ = ["all_callables"]

def callable_with_argument_and_keyword_only_argument(a : int,*, b : int) -> None: pass

def callable_with_all_arguments(a : int, *args : Any, **kwargs : Any) -> None: pass

def callable_with_all_arguments_and_missing_first_annotation(a, *args : Any, **kwargs : Any) -> None: pass

def callable_with_all_arguments_and_missing_second_annotation(a : int, *args, **kwargs : Any) -> None: pass

def callable_with_all_arguments_and_missing_third_annotation(a : int, *args : Any, **kwargs) -> None: pass

def callable_with_argument_and_kwargs(a : int, **kwargs : Any) -> None: pass

def callable_with_argument_and_args(a : int, *args : Any) -> None: pass

def callable_with_kwargs( **kwargs : Any) -> None: pass

def callable_with_args( *args : Any) -> None: pass

def callable_with_keyword_only(*, a : int) -> None: pass

def callable_with_multiple_keyword_only(*, a : int, b : int) -> None: pass

def callable_with_argument_and_multiple_keyword_only(a : int,*, b : int, c : int) -> None: pass

def callable_with_multiple_arguments_and_multiple_keyword_only(a : int, b : int,*, c : int, d : int) -> None: pass

def callable_with_multiple_arguments_and_keyword_only(a : int, b : int,*, c : int) -> None: pass

def callable_with_multiple_arguments_and_kwargs(a : int, b : int, **kwargs : Any) -> None: pass

def callable_with_multiple_arguments_and_args(a : int, b : int, *args : Any) -> None: pass

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