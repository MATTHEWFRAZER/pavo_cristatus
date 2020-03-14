import logging
import pickle

from pavo_cristatus.repositories.data_item import DataItem
from pavo_cristatus.utilities import get_data_item_id

logger = logging.getLogger(__name__)

__all__ = ["read_data_item", "write_data_item"]

def get_data_item(module_qualname, symbol):
    data_item_id = "{0}.{1}".format(module_qualname, symbol.qualname)
    data_item_data = pickle.dumps(symbol.arg_spec)
    data_item = DataItem(data_item_id, data_item_data)
    return data_item

def read_data_item(module_symbols, symbol, repository, accumulator):
    data_item_id = get_data_item_id(module_symbols.qualname, symbol.qualname)
    data_item = repository.read_data_item(data_item_id)
    if not data_item:
        logger.error("could not successfully operate on data item. data id: {0}".format(data_item_id))
        return False
    accumulator[module_symbols][data_item.id] = pickle.loads(data_item.data)
    return True

def write_data_item(module_symbols, symbol, repository):
    ret = True
    data_item = get_data_item(module_symbols.qualname, symbol)
    if not repository.write_data_item(data_item):
        logger.error("could not successfully operate on data item. data id: {0}".format(data_item.id))
        ret = False
    return ret
