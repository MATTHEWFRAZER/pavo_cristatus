import os

from pavo_cristatus.directory_walk_configuration import DirectoryWalkConfiguration
from pavo_cristatus.interactions.annotated_project_loader_interaction.annotated_project_loader_interaction import interact
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..", "project_fake")).replace("\\", "\\\\")

expected_files = {"__init__.py", "module_fake.py"}

def test_annotated_project_loader_interaction():
    result = interact(DirectoryWalkConfiguration(project_root_path, []))
    assert result.status == PavoCristatusStatus.SUCCESS
    assert all(module_symbols.python_file.file_name in expected_files for module_symbols in result.result)
