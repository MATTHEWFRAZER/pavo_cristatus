from pavo_cristatus.interactions.pavo_cristatus_result_monad.bindee_definition import BindeeDefinition
from pavo_cristatus.interaction_sequence_generators.utilities import get_type_check

__all__ = ["rebuild_all_interaction_sequence_generator"]

def rebuild_all_interaction_sequence_generator(annotated_project_loader_interaction,
                                               symbol_signature_replacer_interaction,
                                               sql_repository_write_interaction):
    is_set = get_type_check(set)
    # given a project root as a string we collect all the modules and relevant symbols
    # along with their arg specs under said project and delivers those to the next interaction
    yield BindeeDefinition(annotated_project_loader_interaction, get_type_check(str), is_set)
    # replace the module's symbol signatures with their non annotated form
    yield BindeeDefinition(symbol_signature_replacer_interaction, is_set, is_set)
    # given modules and symbols write/overwrite into our data repository (TODO: should be bool)
    yield BindeeDefinition(sql_repository_write_interaction, is_set, is_set)#get_type_check(bool))