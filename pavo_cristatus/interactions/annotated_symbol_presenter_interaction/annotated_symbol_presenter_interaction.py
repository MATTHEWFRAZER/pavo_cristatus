from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

__all__ = ["interact"]

def interact(project_symbols_annotated_data_items, presentation_strategy):
    """
    interaction that presents annotated symbols
    :param project_symbols_annotated_data_items: all the necessary information for the presentation_strategy to work
    :param presentation_strategy: the way in which the annotated symbol data will be presented
    :return: a bool within a result that will be manipulated with in the PavoCristatusMonad
    """
    if presentation_strategy(project_symbols_annotated_data_items):
        return PavoCristatusResult(True, PavoCristatusStatus.SUCCESS)
    else:
        return PavoCristatusResult(False, PavoCristatusStatus.FAILURE, "could not replace symbols")
