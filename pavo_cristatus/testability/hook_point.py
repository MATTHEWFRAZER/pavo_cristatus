class HookPoint:
    hooks = {}

    @classmethod
    def register(cls, hook_name, hook):
        cls.hooks[hook_name] = hook

    @classmethod
    def call(cls, to_hook_name, to_hook, *args, **kwargs):
        hook = cls.hooks.get(to_hook_name)
        if hook is not None:
            return hook(*args, **kwargs)
        return to_hook(*args, *kwargs)
