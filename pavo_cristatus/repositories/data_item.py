from pavo_cristatus.compression import decompress, compress


class DataItem(object):
    """
    wrapper around the content we put in a backing store
    """

    def __init__(self, id, data):
        self.id = id
        self._data = data

    @property
    def data(self) -> str:
        return decompress(self._data)

    @data.setter
    def data(self ,value : str) -> None:
        _data = compress(value)
