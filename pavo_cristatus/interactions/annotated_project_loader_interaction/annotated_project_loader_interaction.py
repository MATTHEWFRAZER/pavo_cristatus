from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.project_loader.project_loader import load_annotated_project

__all__ = ["interact"]


def interact(project_root):
    """
    :param project_root: root of the project source
    :return: a set of ModuleSymbols within a result that will be manipulated with in the PavoCristatusMonad
    """
    try:
        return PavoCristatusResult(load_annotated_project(project_root), PavoCristatusStatus.SUCCESS)
    except Exception as ex:
        return PavoCristatusResult(None, PavoCristatusStatus.FAILURE, ex.message)