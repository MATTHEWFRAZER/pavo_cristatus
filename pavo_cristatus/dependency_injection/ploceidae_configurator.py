import functools

from ploceidae.utilities.dependency_visibility_enum import DependencyVisibilityEnum
from ploceidae.core.configurators.basic_configurator import BasicConfigurator

__all__ = ["pavo_cristatus_container", "pavo_cristatus_dependency_wrapper"]

basic_configurator = BasicConfigurator()
pavo_cristatus_container = basic_configurator.get_container()
pavo_cristatus_dependency_wrapper = functools.partial(basic_configurator.get_dependency_wrapper(), visibility=DependencyVisibilityEnum.GLOBAL)
