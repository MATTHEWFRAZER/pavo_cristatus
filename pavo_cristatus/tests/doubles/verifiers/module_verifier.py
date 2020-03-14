from pavo_cristatus.python_file import PythonFile

from picidae import lazily_echo


class ModuleVerifier(object):
    def __init__(self, stub_module):
        self.stub_module = stub_module
        self.symbols_of_interest = []
        self.non_symbols_of_interest = []
        self.symbols_of_interest_type = None

    def add_expected_symbol_of_interest(self, symbol_of_interest):
        self.symbols_of_interest.append(symbol_of_interest)
        return self

    def add_expected_non_symbol_of_interest(self, non_symbol_of_interest):
        self.non_symbols_of_interest.append(non_symbol_of_interest)
        return self

    def set_expected_symbols_of_interest_type(self, symbols_of_interest_type):
        self.symbols_of_interest_type = symbols_of_interest_type
        return self

    def verify(self, project_loader, monkey_patcher):
        monkey_patcher(lazily_echo(self.stub_module), lazily_echo([PythonFile(str(), str())]))

        project_symbols = project_loader.load_annotated_project(str())

        assert len(project_symbols) == len(self.symbols_of_interest)
        module_symbols = next(iter(project_symbols)).symbols.get(self.stub_module.__name__, tuple())
        python_symbols = {x.symbol for x in module_symbols}

        if self.symbols_of_interest:
            all(x in python_symbols for x in self.symbols_of_interest)

        if self.non_symbols_of_interest:
            assert all(x not in python_symbols for x in self.non_symbols_of_interest)

        assert all(type(x) is self.symbols_of_interest_type for x in module_symbols)