from __future__ import unicode_literals
from stat_file_source.handler.base_key_value_handler import BaseKeyValueHandler

class AggregateKeyValueHandler(BaseKeyValueHandler):

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool,
    # key_transformer: str, str, State -> str,
    # aggregate_fun: object, str -> object,
    # item_init_value: object
    # rt: AggregateKeyValueHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value):
        super(AggregateKeyValueHandler, self).__init__(key_value_delimiter, known_key_predicate, key_transformer, item_init_value)
        self._aggregate_fun = aggregate_fun

    # spec:
    # key_value_delimiter: str
    # known_key_list: [str]
    # key_transformer: str, str, State -> str,
    # aggregate_fun: object, str -> object,
    # item_init_value: object
    # rt: AggregateKeyValueHandler
    @classmethod
    def create_with_known_key_list(cls, key_value_delimiter, known_key_list, key_transformer, aggregate_fun, item_init_value):
        return cls(key_value_delimiter, lambda key, state: key in known_key_list, key_transformer, aggregate_fun, item_init_value)

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool,
    # key_transformer: str, str, State -> str,
    # aggregate_fun: object, str -> object,
    # item_init_value: object
    # rt: AggregateKeyValueHandler
    @classmethod
    def create_with_known_key_predicate(cls, key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value):
        return cls(key_value_delimiter, known_key_predicate, key_transformer, aggregate_fun, item_init_value)

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        return self._aggregate_fun(old_value, item_value)

__author__ = 'andrey.ushakov'
