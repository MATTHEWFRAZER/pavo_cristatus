from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol

from picidae import access_attribute

__all__ = ["ClassSymbol"]

class ClassSymbol(AbstractSymbol):

    def get_current_source(self, get_current_source_of_symbol, *args):
        lines = self.source.split("\n")
        for symbol in self.nested_symbols:
            line_number = symbol.find_line_number_of_symbol_in_source(self.source)

            if line_number < 0:
                raise ValueError("source dos not contain a line number for {0}".format(symbol))

            current_source = get_current_source_of_symbol(symbol)(*args)
            for line in current_source.split("\n"):
                lines[line_number] = line
                line_number += 1
        return "\n".join(lines)

    def get_non_annotated_source(self):
        return self.get_current_source(access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, module_annotated_data_items):
        return self.get_current_source(access_attribute(self.get_annotated_source.__name__), module_annotated_data_items)


