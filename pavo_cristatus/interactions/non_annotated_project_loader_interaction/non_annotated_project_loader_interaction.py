from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

from pavo_cristatus.project_loader.project_loader import load_non_annotated_project

__all__ = ["interact"]


def interact(project_root_path):
    try:
        return PavoCristatusResult(load_non_annotated_project(project_root_path), PavoCristatusStatus.SUCCESS)
    except Exception as ex:
        return PavoCristatusResult(None, PavoCristatusStatus.FAILURE, ex.message)