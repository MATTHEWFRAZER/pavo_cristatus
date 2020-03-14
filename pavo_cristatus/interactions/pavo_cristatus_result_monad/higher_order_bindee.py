from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_null_result import PavoCristatusNullResult
from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus

__all__ = ["HigherOrderBindee"]

class HigherOrderBindee(object):
    def __init__(self, bindee_definition):
        self.bindee_definition = bindee_definition

    def __call__(self, in_parameter):
        if not self.bindee_definition.in_parameter_predicate(in_parameter):
            raise TypeError("actual in parameter does not align with expected")

        out_result = self.bindee_definition.bindee_function(in_parameter)

        if not self.bindee_definition.out_parameter_predicate(out_result.result):
            raise TypeError("actual out parameter does not align with expected")

        if out_result.status == PavoCristatusStatus.FAILURE:
            return PavoCristatusNullResult("failed in {0}: {1}".format(self.bindee_definition.value_name_to_patch_in, out_result.message))
        return PavoCristatusResultMonad(out_result.result)