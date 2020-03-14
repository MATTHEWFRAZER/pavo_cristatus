import pytest

from picidae import echo, lazily_compose_given_functions

from pavo_cristatus.interaction_sequence_generators.utilities import get_type_check
from pavo_cristatus.interactions.pavo_cristatus_result import PavoCristatusResult
from pavo_cristatus.interactions.pavo_cristatus_result_monad.bindee_definition import BindeeDefinition
from pavo_cristatus.interactions.pavo_cristatus_result_monad.higher_order_bindee import HigherOrderBindee
from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus


class TestHigherOrderBindee:
    @pytest.mark.xfail(raises=TypeError)
    def test_type_missmatch_before_invocation_raises_exception(self):
        bindee_function = lazily_compose_given_functions(echo, lambda x: PavoCristatusResult(x, PavoCristatusStatus.SUCCESS))
        bindee_definition = BindeeDefinition(bindee_function, get_type_check(str), get_type_check(str))
        bindee = HigherOrderBindee(bindee_definition)
        bindee(bool())

    @pytest.mark.xfail(raises=TypeError)
    def test_type_missmatch_after_invocation_raises_exception(self):
        bindee_function = lambda _: PavoCristatusResult(bool(), PavoCristatusStatus.SUCCESS)
        bindee_definition = BindeeDefinition(bindee_function, get_type_check(str), get_type_check(str))
        bindee = HigherOrderBindee(bindee_definition)
        bindee(str())