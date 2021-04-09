import logging
import pickle
import base64

from pavo_cristatus.repositories.data_item import DataItem
from pavo_cristatus.utilities import create_data_item_id

logger = logging.getLogger(__name__)

__all__ = ["read_data_item", "write_data_item"]

def create_data_item(module_qualname, symbol):
    """
    construct a new data item
    :param module_qualname: module qualname of symbol that will be represented by a data item
    :param symbol: symbol object from which we use an arg_spec
    :return: new data item
    """
    data_item_id = "{0}.{1}".format(module_qualname, symbol.qualname)
    byte_data = pickle.dumps(symbol.arg_spec)
    base64_data = base64.b64encode(byte_data)
    data_item_data = str(base64_data, "utf-8")
    data_item = DataItem(data_item_id, data_item_data)
    return data_item

def read_data_item(module_symbols, symbol, repository, accumulator):
    """
    retrieve data item from repository
    :param module_symbols: module_symbols that we use to retrieve data item
    :param symbol: symbol that we use to retrieve data item
    :param repository: a repository object where we retrieve a data item from
    :param accumulator: accumulates the read data items
    :return: bool
    """
    data_item_id = create_data_item_id(module_symbols.qualname, symbol.qualname)
    data_item = repository.read_data_item(data_item_id)
    if not data_item:
        # TODO: look into this
        #logger.error("could not successfully operate on data item. data id: {0}".format(data_item_id))
        #return False
        return True
    data_item_data = base64.b64decode(data_item.data)
    accumulator[module_symbols][data_item.id] = pickle.loads(data_item_data)
    return True

def write_data_item(module_symbols, symbol, repository):
    """
    write data item to repository
    :param module_symbols: module_symbols that we use to write a data item
    :param symbol: symbol that we use to write a data item
    :param repository: a repository object where we write a data item to
    :return: bool
    """
    ret = True
    data_item = create_data_item(module_symbols.qualname, symbol)
    if not repository.write_data_item(data_item):
        logger.error("could not successfully operate on data item. data id: {0}".format(data_item.id))
        ret = False
    return ret
