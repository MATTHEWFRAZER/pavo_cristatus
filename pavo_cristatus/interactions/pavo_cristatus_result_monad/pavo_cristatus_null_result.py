from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad

__all__ = ["PavoCristatusNullResult"]

class PavoCristatusNullResult(PavoCristatusResultMonad):
    def bind(self, _):
        return self