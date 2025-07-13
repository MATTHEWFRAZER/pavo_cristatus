import os
from typing import Callable, Any

from picidae import access_attribute

__all__ = ["ModuleSymbols"]

from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import pavo_cristatus_get_source_for_module, pavo_cristatus_split


class ModuleSymbols(object):
    """
    data structure that associates a dictionary of interesting symbols with the module object, PythonFile object, and module qualname
    """
    def __init__(self, module, python_file, qualname, symbol_objects):
        self.module = module
        self.python_file = python_file
        self.qualname = qualname
        self.symbol_objects = symbol_objects

    @property
    def path(self) -> str:
        """get the full path of the module"""
        return os.path.join(self.python_file.package_path, self.python_file.file_name)

    def get_source(self, get_source_strategy, *args):
        """
        gets the source of a module
        :param get_source_strategy: the strategy (e.g. get_annotated_source) for getting the symbol's source
        :param args: contextual data for get_source_strategy
        :return: module source as a string
        """
        source = pavo_cristatus_get_source_for_module(self.module)
        source_lines = pavo_cristatus_split(source)  # TODO: figure out why os.linesep does not work
        for symbol_object in self.symbol_objects:
            line_number = symbol_object.find_line_number_of_symbol_in_module()

            current_source = get_source_strategy(symbol_object)(*args)
            for line in pavo_cristatus_split(current_source):
                source_lines[line_number] = line
                line_number += 1
        return "\n".join(source_lines)


    def get_non_annotated_source(self):
        """
        gets the non annotated source of a module
        :return: the modules's non annotated source as a string
        """
        return self.get_source(access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, old_project_symbols):
        """
        gets the annotated source of a module
        :return: the modules's annotated source as a string
        """
        return self.get_source(access_attribute(self.get_annotated_source.__name__), old_project_symbols)


