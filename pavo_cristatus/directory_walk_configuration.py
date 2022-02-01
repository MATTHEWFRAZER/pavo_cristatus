from typing import List


class DirectoryWalkConfiguration(object):
    def __init__(self, project_root_path, directories_to_ignore):
        self.project_root_path = project_root_path
        self.directories_to_ignore = directories_to_ignore
