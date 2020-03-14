from pavo_cristatus.interactions.pavo_cristatus_result_monad.pavo_cristatus_result_monad import PavoCristatusResultMonad

class TestPavoCristatusResultMonad:
    def test_left_identity(self):
        value = 10
        func = lambda x: PavoCristatusResultMonad(x + 5)
        monad = PavoCristatusResultMonad(value)
        assert monad.bind(func) == func(value)

    def test_right_identity(self):
        monad = PavoCristatusResultMonad(3)
        assert monad.bind(PavoCristatusResultMonad) == monad

    def test_associativity(self):
        value = 1
        f = lambda x: PavoCristatusResultMonad(x + 5)
        g = lambda x: PavoCristatusResultMonad(x + 10)

        monad = PavoCristatusResultMonad(value)
        assert monad.bind(f).bind(g) == monad.bind(lambda x: f(x).bind(g))
