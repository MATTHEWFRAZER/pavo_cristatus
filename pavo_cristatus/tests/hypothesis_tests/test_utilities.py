from hypothesis import given, reject, example, assume
from hypothesis.strategies import text, lists, builds

from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import convert_python_file_to_module_qualname

dummy_python_file = builds(PythonFile, text(), text())

@given(text(), dummy_python_file)
#@example(str(), PythonFile(str(), str()))
def test_convert_python_file_to_module_qualname(project_root_path, python_file):
    #try:
    if any( x in project_root_path for x in ("+", ")", "(", "[", "]", "-", "*", "$", "?")):
        reject()
    convert_python_file_to_module_qualname(project_root_path, python_file)
    #except:
    #    reject()
