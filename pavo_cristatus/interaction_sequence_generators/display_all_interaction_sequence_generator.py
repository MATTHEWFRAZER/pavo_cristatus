from collections import defaultdict

from pavo_cristatus.interactions.pavo_cristatus_result_monad.bindee_definition import BindeeDefinition
from pavo_cristatus.interaction_sequence_generators.utilities import get_type_check

__all__ = ["display_all_interaction_sequence_generator"]

def display_all_interaction_sequence_generator(non_annotated_project_loader_interaction,
                                               sql_repository_read_interaction,
                                               symbol_signature_restorer_interaction,
                                               annotated_symbol_presenter_interaction):
    """
    This generator of interactions will be manipulated by the PavoCristatusMonad
    :param non_annotated_project_loader_interaction: collect all non annotated symbols in a project
    :param sql_repository_read_interaction: collect all the symbols type hint information
    :param symbol_signature_restorer_interaction: restores the symbols to their previous annotated form
    :param annotated_symbol_presenter_interaction: presents the annotated symbols to the user
    """
    is_set = get_type_check(set)
    is_defaultdict = get_type_check(defaultdict)
    # given a project root as a string we collect all the modules and relevant symbols under said project
    # and deliver to the next interaction
    yield BindeeDefinition(non_annotated_project_loader_interaction, get_type_check(str), is_set)
    # given a project root as a string we collect all the modules and relevant symbols under said project and
    # deliver to the next interaction
    yield BindeeDefinition(sql_repository_read_interaction, is_set, is_defaultdict)
    # given a dictionary of symbols associated with their arg specs reconstruct annotated symbols
    yield BindeeDefinition(symbol_signature_restorer_interaction, is_defaultdict, is_defaultdict)
    # given symbol of interests original type annotated form present each symbol as they appear in the project
    yield BindeeDefinition(annotated_symbol_presenter_interaction, is_defaultdict, get_type_check(bool))
