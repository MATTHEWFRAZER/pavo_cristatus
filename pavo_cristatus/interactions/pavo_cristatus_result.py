from typing import Any


class PavoCristatusResult(object):
    """
    result wrapper that has a success flag for PavoCristatusMonad
    """
    def __init__(self, result, status, message = None):
        self.result = result
        self.status = status
        self.message = message
