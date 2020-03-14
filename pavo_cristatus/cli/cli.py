import argparse
import operator
import os

from trochilidae.interoperable_reduce import interoperable_reduce
from trochilidae.interoperable_map import interoperable_map

from pavo_cristatus.interaction_sequence_generators import rebuild_all_interaction_sequence_generator
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_container, pavo_cristatus_dependency_wrapper
from pavo_cristatus.interaction_sequence_generators.display_all_interaction_sequence_generator import \
    display_all_interaction_sequence_generator
from pavo_cristatus.interactions.pavo_cristatus_result_monad.higher_order_bindee import HigherOrderBindee
from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

parser = argparse.ArgumentParser(description="pavo cristatus cli")
subparsers = parser.add_subparsers()
rebuild_all_subparser = subparsers.add_parser("RebuildAll")
rebuild_all_subparser.add_argument("--project-root", type=str, required=True)
rebuild_all_subparser.add_argument("--database-path", type=str, default=None)

def main():
    arguments = parser.parse_args()
    project_root = arguments.project_root
    database_path = arguments.database_path

    if database_path is None:
        database_path = os.path.join(project_root, "pavo_cristatus.db")

    # register project root and database path as a dependencies so it can be resolved to some of the transitive
    # dependencies later on in the sequence
    pavo_cristatus_dependency_wrapper(resolvable_name="project_root")(lambda: project_root)
    pavo_cristatus_dependency_wrapper(resolvable_name="database_path")(lambda: database_path)

    if arguments.rebuild_all:
        sequence_name = "rebuild all"
        initial_argument = project_root
        generator = pavo_cristatus_container.resolve_dependencies(rebuild_all_interaction_sequence_generator)
    elif arguments.display_all:
        sequence_name = "display_all"
        initial_argument = project_root
        generator = pavo_cristatus_container.resolve_dependencies(display_all_interaction_sequence_generator)
    else:
        print("invalid operation")
        exit(1)

    result = interoperable_reduce(operator.rshift, interoperable_map(lambda x: HigherOrderBindee(x).__call__, generator), PavoCristatusResultMonad(initial_argument))
    if result.value_to_patch_in.status == PavoCristatusStatus.SUCCESS:
        print("succesfully completed {0} command".format(sequence_name))
    else:
        print(result.value_to_patch_in.message)


if __name__ == "__main__":
    main()