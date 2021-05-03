__all__ = ["PavoCristatusNamespace"]

# our primary problem is that a decorator can intercept and reset the decorated
# when we chain decorators, we have no access the previous decorators nor the original function
# 1. what we can do is, parse the source that a lambda decorator gives us (skip the @ until we get a def, take the source beyond that)
#    a. what about decorators that have their own source someplace else
# 2. what we

# we also have to see, when we get the source from a lambda decorator. Does it give the full source of decorated function? Does it
# give the full source the decorated class?
class PavoCristatusNamespace(dict):
    """
    class that allows us to hook into, the exec call we make to retrieve symbols.
    currently we don't use this, but it could potentially allow us to detect normal decorators
    """
    def __init__(self, on_set_item, context=None):
        self.on_set_item = on_set_item
        self.context = context
        super().__init__()

    def __setitem__(self, key, value):
        if self.on_set_item(self, key, value, self.context):
            return super().__setitem__(key, value)
        else:
            return None