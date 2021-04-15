import inspect
import os

from picidae import access_attribute

__all__ = ["ModuleSymbols"]

class ModuleSymbols(object):
    """
    data structure that associates a dictionary of interesting symbols with the module object, PythonFile object, and module qualname
    """
    def __init__(self, module, python_file, qualname, symbols):
        self.module = module
        self.python_file = python_file
        self.qualname = qualname
        self.symbols = symbols

    @property
    def path(self):
        """get the full path of the module"""
        return os.path.join(self.python_file.package_path, self.python_file.file_name)

    def get_source(self, get_source_strategy, *args):
        """
        gets the source of a module
        :param get_source_strategy: the strategy (e.g. get_annotated_source) for getting the symbol's source
        :param args: contextual data for get_source_strategy
        :return: module source as a string
        """
        source = inspect.getsource(self.module)
        source_lines = source.split("\n")  # TODO: figure out why os.linesep does not work
        for symbol in self.symbols:
            line_number = symbol.find_line_number_of_symbol_in_source(source)
            current_source = get_source_strategy(symbol)(*args)
            for line in current_source.split("\n"):
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


