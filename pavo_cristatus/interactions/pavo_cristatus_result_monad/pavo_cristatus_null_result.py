from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad

__all__ = ["PavoCristatusNullResult"]

class PavoCristatusNullResult(PavoCristatusResultMonad):
    """
    when we have a failure in the monad, this will be used and will short circuit the program on tracks
    """
    def bind(self, _):
        return self