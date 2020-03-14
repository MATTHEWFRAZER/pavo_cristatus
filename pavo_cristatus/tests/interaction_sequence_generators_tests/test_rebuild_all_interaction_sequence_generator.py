import operator
import os

from picidae import lazily_echo
import pytest
from trochilidae.interoperable_reduce import interoperable_reduce
from trochilidae.interoperable_map import interoperable_map

from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper, \
    pavo_cristatus_container
from pavo_cristatus.interaction_sequence_generators.rebuild_all_interaction_sequence_generator import rebuild_all_interaction_sequence_generator
from pavo_cristatus.interactions.pavo_cristatus_result_monad.higher_order_bindee import HigherOrderBindee
from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad
from pavo_cristatus.tests.doubles.spies.sqlite_cursor_spy import SQLiteCursorSpy
from pavo_cristatus.tests.doubles.spies.sqlite_query_result_spy import SQLiteQueryResultSpy

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..", "project_fake")).replace("\\", "\\\\")

def database_connection():
    sqlite_query_result_spy = SQLiteQueryResultSpy(1, lazily_echo(("id", None)))
    return SQLiteCursorSpy(sqlite_query_result_spy)

def test_display_all_interaction_sequence_generator():

    # register project root and database path as a dependencies so it can be resolved to some of the transitive
    # dependencies later on in the sequence
    pavo_cristatus_dependency_wrapper(visibility="module", resolvable_name="project_root")(lambda: project_root_path)
    pavo_cristatus_dependency_wrapper(visibility="module", resolvable_name="database_path")(lambda: project_root_path)
    pavo_cristatus_dependency_wrapper()(database_connection)

    initial_argument = project_root_path
    generator = pavo_cristatus_container.wire_dependencies(rebuild_all_interaction_sequence_generator)

    try:
        interoperable_reduce(operator.rshift, interoperable_map(lambda x: HigherOrderBindee(x).__call__, generator), PavoCristatusResultMonad(initial_argument))
    except Exception as ex:
        pytest.fail(". Ex {0}".format(ex))