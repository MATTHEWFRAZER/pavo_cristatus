from typing import Any

from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_null_result import PavoCristatusNullResult
from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

__all__ = ["HigherOrderBindee"]

class HigherOrderBindee(object):
    """
    generalizes functions so that they can be lifted into the PavoCristatusMonad, (i.e. lower level functions can remain
    less specialized (a -> b) instead of (a -> Mb)
    the idea is that we can have some safe guards inside of the monad (TODO: these safeguards should run at module load time)
    """
    def __init__(self, bindee_definition):
        self.bindee_definition = bindee_definition

    def __call__(self, in_parameter):
        if not self.bindee_definition.in_parameter_predicate(in_parameter):
            raise TypeError("actual in parameter does not align with expected")

        out_result = self.bindee_definition.bindee_function(in_parameter)

        if out_result.status == PavoCristatusStatus.FAILURE:
            return PavoCristatusNullResult("failed: {0}".format(out_result.message))

        if not self.bindee_definition.out_parameter_predicate(out_result.result):
            raise TypeError("actual out parameter does not align with expected")

        return PavoCristatusResultMonad(out_result.result)
