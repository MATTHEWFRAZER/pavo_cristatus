from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.project_loader.project_loader import load_non_annotated_project

__all__ = ["interact"]


def interact(project_root_path):
    """
    loads non annotated symbols from a project
    :param project_root_path: the project root of the source
    :return: a set of ModuleSymbols within a result that will be manipulated with in the PavoCristatusMonad
    """
    try:
        return PavoCristatusResult(load_non_annotated_project(project_root_path), PavoCristatusStatus.SUCCESS)
    except Exception as ex:
        return PavoCristatusResult(None, PavoCristatusStatus.FAILURE, ex.message)