import argparse
import operator
import os
import sys

sys.path.append(os.path.abspath(os.path.join("", "..")))

from trochilidae.interoperable_reduce import interoperable_reduce
from trochilidae.interoperable_map import interoperable_map

from pavo_cristatus.directory_walk_configuration import DirectoryWalkConfiguration
from pavo_cristatus.interaction_sequence_generators import rebuild_all_interaction_sequence_generator, display_all_interaction_sequence_generator
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_container, pavo_cristatus_dependency_wrapper
from pavo_cristatus.interactions.pavo_cristatus_result_monad.higher_order_bindee import HigherOrderBindee
from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

REBUILD_ALL = "rebuild-all"
DISPLAY_ALL = "display-all"

parser = argparse.ArgumentParser(description="pavo cristatus cli")
parser.add_argument("--subparser-choice", type=str, required=True, choices=[REBUILD_ALL, DISPLAY_ALL], dest="subparser_choice")
parser.add_argument("--project-root-path", type=str, required=True, dest="project_root_path")
parser.add_argument("--database-path", type=str, default=None, dest="database_path")
parser.add_argument("-i", "--directory-to-ignore", type=str, default=None, dest="directory_to_ignore")
# TODO: leaving these incase we need a subparser (had to figure this out by trial and error since there are no examples out there)
#subparsers = parser.add_subparsers()
#pavo_cristatus_subparser = subparsers.add_parser("SubParser")
#pavo_cristatus_subparser.add_argument("--project-root", type=str, required=True, dest="project_root")
#pavo_cristatus_subparser.add_argument("--database-path", type=str, default=None, dest="database_path")

def main():
    arguments = parser.parse_args()
    subparser_choice = arguments.subparser_choice
    project_root_path = os.path.abspath(arguments.project_root_path)
    database_path = arguments.database_path
    directory_to_ignore = arguments.directory_to_ignore

    directories_to_ignore = []
    if directory_to_ignore is not None:
        directories_to_ignore.append(os.path.abspath(directory_to_ignore))

    #TODO: see above
    #arguments = pavo_cristatus_subparser.parse_args()
    #project_root = os.path.abspath(arguments.project_root)
    #database_path = arguments.database_path

    if database_path is None:
        database_path = os.path.join(project_root_path, "pavo_cristatus.db")

    # register project root and database path as a dependencies so it can be resolved to some of the transitive
    # dependencies later on in the sequence
    pavo_cristatus_dependency_wrapper(resolvable_name="project_root")(lambda: project_root_path)
    pavo_cristatus_dependency_wrapper(resolvable_name="database_path")(lambda: database_path)

    initial_argument = DirectoryWalkConfiguration(project_root_path, directories_to_ignore)
    if subparser_choice == REBUILD_ALL:
        sequence_name = REBUILD_ALL
        generator = pavo_cristatus_container.wire_dependencies(rebuild_all_interaction_sequence_generator)
    elif subparser_choice == DISPLAY_ALL:
        sequence_name = DISPLAY_ALL
        generator = pavo_cristatus_container.wire_dependencies(display_all_interaction_sequence_generator)
    else:
        print("invalid operation")
        exit(-1)


    result = interoperable_reduce(operator.rshift, interoperable_map(lambda x: HigherOrderBindee(x).__call__, generator), PavoCristatusResultMonad(initial_argument))
    if result.is_success():
        print("successfully completed {0} command".format(sequence_name))
    else:
        print(result.value)


if __name__ == "__main__":
    main()
