import inspect
import os

from picidae import access_attribute

__all__ = ["ModuleSymbols"]

class ModuleSymbols(object):
    def __init__(self, module, python_file, qualname, symbols):
        self.module = module
        self.python_file = python_file
        self.qualname = qualname
        self.symbols = symbols

    @property
    def path(self):
        return os.path.join(self.python_file.package_path, self.python_file.file_name)

    def get_current_source(self, get_current_source_of_symbol, *args):
        source = inspect.getsource(self.module)
        source_lines = source.split()
        for symbol in self.symbols:
            line_number = symbol.find_line_number_of_symbol_in_source(source)
            current_source = get_current_source_of_symbol(symbol)(*args)
            for line in current_source.split():
                source_lines[line_number] = line
                line_number += 1
        return "\n".join(source_lines)


    def get_non_annotated_source(self):
        return self.get_current_source(access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, old_project_symbols):
        return self.get_current_source(access_attribute(self.get_annotated_source.__name__), old_project_symbols)


