from __future__ import unicode_literals
from src.handler.base_key_value_handler import BaseKeyValueHandler

class AggregateKeyValueHandler(BaseKeyValueHandler):

    def __init__(self, key_value_delimiter, known_keys, aggregate_fun):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_keys)
        self._aggregate_fun = aggregate_fun

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        return self._aggregate_fun(old_value, item_value)

    _aggregate_fun = None

__author__ = 'andrey.ushakov'
