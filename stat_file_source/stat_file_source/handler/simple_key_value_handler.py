from __future__ import unicode_literals
from stat_file_source.handler.base_key_value_handler import BaseKeyValueHandler

class SimpleKeyValueHandler(BaseKeyValueHandler):

    # spec: str, (str, State -> bool), (str, State -> str) -> SimpleKeyValueHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer):
        super(SimpleKeyValueHandler, self).__init__(key_value_delimiter, known_key_predicate, key_transformer, [])

    # spec: str, [str], (str, State -> str) -> SimpleKeyValueHandler
    @classmethod
    def create_with_known_key_list(cls, key_value_delimiter, known_key_list, key_transformer):
        return cls(key_value_delimiter, lambda key, state: key in known_key_list, key_transformer)

    # spec: str, (str, State -> bool), (str, State -> str) -> SimpleKeyValueHandler
    @classmethod
    def create_with_known_key_predicate(cls, key_value_delimiter, known_key_predicate, key_transformer):
        return cls(key_value_delimiter, known_key_predicate, key_transformer)

    # spec: [str], str -> [str]
    def _define_value(self, old_value, item_value):
        new_value = list(old_value)
        new_value.append(item_value)
        return new_value

__author__ = 'andrey.ushakov'
