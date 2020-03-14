from pavo_cristatus.project_loader import project_loader
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper

from picidae import access_attribute

dependency_module_name = "project_loader"

__all__ = [dependency_module_name]

pavo_cristatus_dependency_wrapper(resolvable_name="annotated_" + dependency_module_name,
                                  transformation=access_attribute("load_annotated_project"))(lambda: project_loader)

pavo_cristatus_dependency_wrapper(resolvable_name="non_annotated_" + dependency_module_name,
                                  transformation=access_attribute("load_non_annotated_project"))(lambda: project_loader)