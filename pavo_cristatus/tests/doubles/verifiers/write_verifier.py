class WriteVerifier(object):
    def reset(self, expected):
        self.expected = expected

    def write(self, actual):
        self.actual = actual

    def __call__(self, actual):
        self.actual = actual

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def verify(self):
        assert self.expected == self.actual