from collections import defaultdict

from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.symbol_signature_restorer import symbol_signature_restorer

__all__ = ["interact"]

def interact(project_symbols_annotated_data_items):
    if symbol_signature_restorer.restore(project_symbols_annotated_data_items):
        return PavoCristatusResult(project_symbols_annotated_data_items, PavoCristatusStatus.SUCCESS)
    else:
        return PavoCristatusResult(project_symbols_annotated_data_items, PavoCristatusStatus.FAILURE, "could not restore symbols")
