from pymonad import Monad

__all__ = ["PavoCristatusResultMonad"]

class PavoCristatusResultMonad(Monad):
    """monad used to process the projects that need to be converted from annotated to unannotated and visa versa"""

    def bind(self, function):
        return function(self.value)