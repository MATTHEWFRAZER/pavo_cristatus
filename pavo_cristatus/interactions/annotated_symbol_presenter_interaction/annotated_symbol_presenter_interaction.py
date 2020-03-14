from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

__all__ = ["interact"]

def interact(project_symbols_annotated_data_items, presentation_strategy):
    if presentation_strategy(project_symbols_annotated_data_items):
        return PavoCristatusResult(True, PavoCristatusStatus.SUCCESS)
    else:
        return PavoCristatusResult(False, PavoCristatusStatus.FAILURE, "could not replace symbols")
