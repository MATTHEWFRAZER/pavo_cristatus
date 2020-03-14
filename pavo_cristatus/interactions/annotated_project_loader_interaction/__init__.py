from pavo_cristatus.interactions.annotated_project_loader_interaction import annotated_project_loader_interaction
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper
from pavo_cristatus.utilities import access_interaction_callable

dependency_module_name = "annotated_project_loader_interaction"

__all__ = [dependency_module_name]

pavo_cristatus_dependency_wrapper(resolvable_name=dependency_module_name,
                                  transformation=access_interaction_callable)(lambda: annotated_project_loader_interaction)