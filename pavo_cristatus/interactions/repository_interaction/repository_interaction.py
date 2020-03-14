from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

__all__ = ["RepositoryInteraction"]

class RepositoryInteraction(object):
    def __init__(self, repository, operation, get_accumulator):
        self.repository = repository
        self.operation = operation
        self.get_accumulator = get_accumulator

    def interact(self, project_symbols):
        """
        :param project_symbols: a dictionary of modules associated with their symbols
        :return: bool
        """
        accumulator = self.get_accumulator()
        for module_symbols in project_symbols:
            for symbol in module_symbols.symbols:
                if not self.operation(module_symbols, symbol, self.repository, accumulator):
                    return PavoCristatusResult(project_symbols, PavoCristatusStatus.FAILURE, "failed with operation {0}".format(self.operation))
                for nested_symbol in symbol.nested_symbols:
                    if not self.operation(module_symbols, nested_symbol, self.repository, accumulator):
                        return PavoCristatusResult(project_symbols, PavoCristatusStatus.FAILURE,
                                                   "failed with operation {0}".format(self.operation))
        # needs to be an explicit check for equality for False (TODO: fix this)
        ret = accumulator
        if accumulator == False:
            ret = project_symbols
        return PavoCristatusResult(ret, PavoCristatusStatus.SUCCESS)
