from pymonad import Monad

__all__ = ["PavoCristatusResultMonad"]

class PavoCristatusResultMonad(Monad):

    def bind(self, function):
        return function(self.value)