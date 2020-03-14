from pavo_cristatus.compression import decompress, compress


class DataItem(object):
    def __init__(self, id, data):
        self.id = id
        self._data = data

    @property
    def data(self):
        return decompress(self._data)

    @data.setter
    def data(self ,value):
        _data = compress(value)