from typing import Any

from pavo_cristatus.utilities import pavo_cristatus_get_source_for_module


class NormalizedModuleSymbol(object):
    def __init__(self, module):
        self.symbol = module
        self.source = pavo_cristatus_get_source_for_module(module)
        self.file = module.__file__
        self.module = module.__name__
