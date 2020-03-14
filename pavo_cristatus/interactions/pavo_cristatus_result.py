class PavoCristatusResult(object):
    def __init__(self, result, status, message=None):
        self.result = result
        self.status = status
        self.message = message