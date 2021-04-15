class PythonFile(object):
    """
    object that associates a file name with a package path so that we can construct full paths to python files
    """
    def __init__(self, file_name, package_path):
        self.file_name = file_name
        self.package_path = package_path
