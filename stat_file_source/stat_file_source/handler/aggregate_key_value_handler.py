from __future__ import unicode_literals
from stat_file_source.handler.base_key_value_handler import BaseKeyValueHandler

class AggregateKeyValueHandler(BaseKeyValueHandler):

    # spec: str, (str, State -> bool), (str, State -> str), (object, str -> object) -> AggregateKeyValueHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_key_predicate, key_transformer, item_init_value)
        self._aggregate_fun = aggregate_fun

    # spec: str, [str], (str, State -> str), (object, str -> object) -> AggregateKeyValueHandler
    @staticmethod
    def create_with_known_key_list(key_value_delimiter, known_key_list, key_transformer, aggregate_fun, item_init_value):
        return AggregateKeyValueHandler(key_value_delimiter, lambda key, state: key in known_key_list, key_transformer, aggregate_fun, item_init_value)

    # spec: str, (str, State -> bool), (str, State -> str), (object, str -> object) -> AggregateKeyValueHandler
    @staticmethod
    def create_with_known_key_predicate(key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value):
        return AggregateKeyValueHandler(key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value)

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        return self._aggregate_fun(old_value, item_value)

    _aggregate_fun = None

__author__ = 'andrey.ushakov'
