from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol

from picidae import access_attribute

__all__ = ["ClassSymbol"]

from pavo_cristatus.utilities import pavo_cristatus_split, is_decorator_line


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
        lines = pavo_cristatus_split(self.source)

        line_number = self.normalized_symbol.find_line_number_of_symbol_in_source(self.source)
        if line_number < 0:
            raise ValueError("source does not contain a line number for {0}".format(self.name))

        # TODO: HACK ALERT, root cause this
        if not is_decorator_line(lines[0]):
            lines[line_number] = self.normalized_symbol.indent + lines[line_number]

        for symbol_object in self.nested_symbols:
            line_number = symbol_object.find_line_number_of_symbol_in_source(self.source)

            if line_number < 0:
                raise ValueError("source does not contain a line number for {0}".format(symbol_object.name))

            current_source = get_source_strategy(symbol_object)(*args).rstrip()
            for line in pavo_cristatus_split(current_source):
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


