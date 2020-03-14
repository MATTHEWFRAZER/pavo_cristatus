class AttributeVerifier(object):
    def __init__(self, attribute_accessor, expected_value):
        self.attribute_accessor = attribute_accessor
        self.expected_value = expected_value

    def verify(self, to_verify):
        assert self.attribute_accessor(to_verify) == self.expected_value