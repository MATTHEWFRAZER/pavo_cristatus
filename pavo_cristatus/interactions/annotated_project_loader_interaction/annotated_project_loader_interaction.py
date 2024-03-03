import traceback

from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.project_loader.project_loader import load_annotated_project

__all__ = ["interact"]


def interact(directory_walk_configuration):
    """
    :param project_root: root of the project source
    :return: a set of ModuleSymbols within a result that will be manipulated with in the PavoCristatusMonad
    """
    try:
        return PavoCristatusResult(load_annotated_project(directory_walk_configuration.project_root_path, directory_walk_configuration.directories_to_ignore), PavoCristatusStatus.SUCCESS)
    except Exception as ex:
        return PavoCristatusResult(None, PavoCristatusStatus.FAILURE, traceback.format_exc())
