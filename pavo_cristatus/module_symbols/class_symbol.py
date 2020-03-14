from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol

from picidae import access_attribute

__all__ = ["ClassSymbol"]

class ClassSymbol(AbstractSymbol):
    """
    represents a class as a symbol object
    """

    def get_source(self, get_source_strategy, *args):
        """
        gets the source of a class symbol
        :param get_source_strategy: the strategy (e.g. get_annotated_source) for getting the symbol's source
        :param args: contextual data for get_source_strategy
        :return: the symbol's source as a string
        """
        lines = self.source.split("\n")
        for symbol in self.nested_symbols:
            line_number = symbol.find_line_number_of_symbol_in_source(self.source)

            if line_number < 0:
                raise ValueError("source dos not contain a line number for {0}".format(symbol))

            current_source = get_source_strategy(symbol)(*args)
            for line in current_source.split("\n"):
                lines[line_number] = line
                line_number += 1
        return "\n".join(lines)

    def get_non_annotated_source(self):
        """
        gets the non annotated source of a symbol
        :return: the symbol's source as a string
        """
        return self.get_source(access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, module_annotated_data_items):
        """
        gets the annotated source of a symbol
        :return: the symbol's source as a string
        """
        return self.get_source(access_attribute(self.get_annotated_source.__name__), module_annotated_data_items)


