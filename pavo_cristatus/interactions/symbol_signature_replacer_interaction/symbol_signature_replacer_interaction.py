from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.symbol_signature_replacer import symbol_signature_replacer

__all__ = ["interact"]

def interact(project_symbols):
    if symbol_signature_replacer.replace(project_symbols):
        return PavoCristatusResult(project_symbols, PavoCristatusStatus.SUCCESS)
    else:
        return PavoCristatusResult(project_symbols, PavoCristatusStatus.FAILURE, "could not replace symbols")

