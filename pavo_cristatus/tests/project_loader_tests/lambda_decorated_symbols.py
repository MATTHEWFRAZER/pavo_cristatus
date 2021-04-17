__all__ = ["lambda_decorated_callable_to_normalize", "LambdaDecoratedClassToNormalize"]

@(lambda f: lambda x: f(x))
def lambda_decorated_callable_to_normalize(x): pass


@(lambda c: lambda: True)
class LambdaDecoratedClassToNormalize: pass