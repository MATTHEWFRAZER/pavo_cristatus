class ModuleFakeClass(type):
    def __new__(mcs, name, bases, attributes):
        class_instance = type.__new__(mcs, name, bases, attributes)
        # need this so that we trick the project loader into believing this is the containing module
        class_instance.__name__ = class_instance.__module__
        return class_instance